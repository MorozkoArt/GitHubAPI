import os
import torch
import joblib
import torch.optim as optim
from torch.utils.data import DataLoader
from pathlib import Path
from GenerationUsers.M_separation_data import separation
from GenerationUsers.C_generation_fake_users import GitHubUserGenerator
from ForModel.C_dataset import GitHubDataset
from ForModel.C_model import GitHubModel
from ForModel.C_loss import ZeroConstrainedLoss
from ForModel.M_education import evaluate, train_epoch

def separator(char="-", width=60):
    print(char * width)


def export_onnx(model: GitHubModel, onnx_path: Path, input_size: int = 28) -> None:
    model.eval()
    dummy = torch.zeros(1, input_size)

    batch_dim = torch.export.Dim("batch_size", min=1, max=1024)
    dynamic_shapes = {"x": {0: batch_dim}}

    torch.onnx.export(
        model,
        dummy,
        str(onnx_path),
        input_names=["input"],
        output_names=["output"],
        dynamic_shapes=dynamic_shapes,
        opset_version=18,
        dynamo=True,
    )
    size_mb = onnx_path.stat().st_size / 1024 / 1024
    print(f"  ONNX saved: {onnx_path}  ({size_mb:.2f} MB)")


def verify_onnx(onnx_path: Path, scaler, X_test_raw) -> None:
    try:
        import onnxruntime as ort

        session    = ort.InferenceSession(str(onnx_path))
        input_name = session.get_inputs()[0].name

        non_zero_mask = (X_test_raw != 0).any(axis=1)
        first_non_zero = X_test_raw[non_zero_mask].iloc[:1]

        sample = scaler.transform(first_non_zero.values).astype("float32")
        out    = session.run(None, {input_name: sample})[0]

        print(f"  ONNX check passed. Sample prediction (first non-zero row):")
        print(f"  {out[0].round(3)}")
    except ImportError:
        print("  onnxruntime not installed in train env, skipping check.")


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Environment variable '{name}' is not set. Check your .env file.")
    return value


def main() -> None:
    separator("=")
    print("GitHub Profile Scorer -- Model Training")
    separator("=")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device : {device}")

    csv_path    = Path(require_env("DATASET_PATH"))
    onnx_path   = Path(require_env("MODEL_PATH"))
    pth_path    = Path(require_env("CHECKPOINT_PATH"))
    scaler_path = Path(require_env("SCALER_PATH"))

    # Создаём папку data если её нет
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Dataset    : {csv_path}")
    print(f"Checkpoint : {pth_path}")
    print(f"ONNX model : {onnx_path}")
    print(f"Scaler     : {scaler_path}")

    separator()
    print("STEP 1 / 5  Dataset")
    separator()

    if not csv_path.exists():
        print("Generating 300 000 synthetic profiles...")
        gen = GitHubUserGenerator()
        df  = gen.generate_users()
        gen.save_to_csv(df, str(csv_path))
        print(f"  Saved: {csv_path}  ({len(df)} rows)")
    else:
        print(f"  Found existing dataset: {csv_path}")

    X_train, y_train, X_val, y_val, X_test, y_test = separation(str(csv_path))
    print(f"  Train: {len(X_train)}  Val: {len(X_val)}  Test: {len(X_test)}")

    separator()
    print("STEP 2 / 5  DataLoaders")
    separator()

    train_ds = GitHubDataset(X_train, y_train, fit_scaler=True)
    scaler   = train_ds.get_scaler()
    val_ds   = GitHubDataset(X_val,   y_val,   scaler=scaler)
    test_ds  = GitHubDataset(X_test,  y_test,  scaler=scaler)

    train_loader = DataLoader(train_ds, batch_size=256, shuffle=True,  num_workers=0)
    val_loader   = DataLoader(val_ds,   batch_size=256, shuffle=False, num_workers=0)
    test_loader  = DataLoader(test_ds,  batch_size=256, shuffle=False, num_workers=0)

    print("  DataLoaders ready.")

    separator()
    print("STEP 3 / 5  Model")
    separator()

    model = GitHubModel(
        input_size=X_train.shape[1],
        output_size=y_train.shape[1],
    ).to(device)

    total_params = sum(p.numel() for p in model.parameters())
    print(f"  Parameters : {total_params:,}")
    print(f"  Input size : {X_train.shape[1]}")
    print(f"  Output size: {y_train.shape[1]}")

    separator()
    print("STEP 4 / 5  Training")
    separator()

    criterion  = ZeroConstrainedLoss(zero_weight=1.5)
    optimizer  = optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
    scheduler  = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=100, eta_min=1e-5)

    best_val_loss  = float("inf")
    patience       = 10
    patience_count = 0
    max_epochs     = 150

    print(f"  Max epochs : {max_epochs}")
    print(f"  Patience   : {patience}")
    print(f"  Zero weight: {criterion.zero_weight}")
    separator()

    header = f"{'Epoch':>6}  {'Train':>8}  {'Val':>8}  {'MAE':>7}  {'R2':>7}  {'LR':>9}  Note"
    print(header)
    separator()

    for epoch in range(1, max_epochs + 1):
        train_loss = train_epoch(model, train_loader, optimizer, criterion, device)
        val_loss, val_mae, val_r2 = evaluate(model, val_loader, criterion, device)
        scheduler.step()

        lr_now = optimizer.param_groups[0]["lr"]
        note   = ""

        if val_loss < best_val_loss:
            best_val_loss  = val_loss
            patience_count = 0
            torch.save(model.state_dict(), str(pth_path))
            note = "[BEST]"
        else:
            patience_count += 1
            if patience_count >= patience:
                print(f"{epoch:>6}  {train_loss:>8.4f}  {val_loss:>8.4f}  "
                      f"{val_mae:>7.4f}  {val_r2:>7.4f}  {lr_now:>9.2e}  [STOP]")
                print(f"\n  Early stopping at epoch {epoch}.")
                break

        print(f"{epoch:>6}  {train_loss:>8.4f}  {val_loss:>8.4f}  "
              f"{val_mae:>7.4f}  {val_r2:>7.4f}  {lr_now:>9.2e}  {note}")

    separator()
    print("STEP 5 / 5  Test + Export")
    separator()

    print("  Loading best checkpoint...")
    model.load_state_dict(torch.load(str(pth_path), map_location=device))
    test_loss, test_mae, test_r2 = evaluate(model, test_loader, criterion, device)

    print(f"  Test loss : {test_loss:.4f}")
    print(f"  Test MAE  : {test_mae:.4f}")
    print(f"  Test R2   : {test_r2:.4f}")

    separator()
    print("  Exporting to ONNX...")
    export_onnx(model, onnx_path, input_size=X_train.shape[1])
    verify_onnx(onnx_path, scaler, X_test)

    joblib.dump(scaler, str(scaler_path))
    size_kb = scaler_path.stat().st_size / 1024
    print(f"  Scaler saved: {scaler_path}  ({size_kb:.1f} KB)")

    separator("=")
    print("Training complete.")
    separator("=")


if __name__ == "__main__":
    main()