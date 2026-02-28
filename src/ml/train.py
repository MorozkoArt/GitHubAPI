import os
import sys
import torch
import torch.optim as optim
from torch.utils.data import DataLoader
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))
sys.path.insert(0, str(_ROOT / "ml"))
sys.path.insert(0, str(_ROOT / "common"))

from GenerationUsers.M_separation_data import separation
from GenerationUsers.C_generation_fake_users import GitHubUserGenerator
from ForModel.C_dataset import GitHubDataset
from ForModel.C_model import GitHubModel
from ForModel.C_loss import ZeroConstrainedLoss
from ForModel.M_education import evaluate, train_epoch

import joblib
import numpy as np
from sklearn.metrics import mean_absolute_error, r2_score


def export_onnx(model: GitHubModel, onnx_path: Path, input_size: int = 28) -> None:
    model.eval()
    dummy = torch.zeros(1, input_size)

    torch.onnx.export(
        model,
        dummy,
        str(onnx_path),
        input_names=["input"],
        output_names=["output"],
        dynamic_axes={
            "input":  {0: "batch_size"},
            "output": {0: "batch_size"},
        },
        opset_version=18,
        do_constant_folding=True,
    )
    size_mb = onnx_path.stat().st_size / 1024 / 1024
    print(f" ONNX модель сохранена: {onnx_path}  ({size_mb:.2f} MB)")


def verify_onnx(onnx_path: Path, scaler, X_test_raw) -> None:
    try:
        import onnxruntime as ort

        session = ort.InferenceSession(str(onnx_path))
        input_name = session.get_inputs()[0].name

        sample = scaler.transform(X_test_raw.values[:5])
        ort_out = session.run(None, {input_name: sample.astype("float32")})[0]

        print(f"  ONNX проверка пройдена. Пример предсказания (строка 0):")
        print(f"    {ort_out[0].round(3)}")
    except ImportError:
        print("  onnxruntime не установлен в среде обучения — пропускаем проверку.")



def main() -> None:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Устройство: {device}")

    data_dir = Path(os.getenv("DATA_DIR"))
    data_dir.mkdir(parents=True, exist_ok=True)

    csv_path    = data_dir / "training.csv"
    onnx_path   = data_dir / "model.onnx"
    pth_path    = data_dir / "best_model.pth"
    scaler_path = data_dir / "scaler.pkl"

    if not csv_path.exists():
        gen = GitHubUserGenerator()
        df  = gen.generate_users()
        gen.save_to_csv(df, str(csv_path))
        print(f"  Датасет сохранён: {csv_path}  ({len(df)} строк)")

    X_train, y_train, X_val, y_val, X_test, y_test = separation(str(csv_path))
    print(f"Размеры выборок: train={len(X_train)}, val={len(X_val)}, test={len(X_test)}")

    train_ds = GitHubDataset(X_train, y_train, fit_scaler=True)
    scaler   = train_ds.get_scaler()

    val_ds   = GitHubDataset(X_val,   y_val,   scaler=scaler)
    test_ds  = GitHubDataset(X_test,  y_test,  scaler=scaler)

    train_loader = DataLoader(train_ds, batch_size=256, shuffle=True,  num_workers=0)
    val_loader   = DataLoader(val_ds,   batch_size=256, shuffle=False, num_workers=0)
    test_loader  = DataLoader(test_ds,  batch_size=256, shuffle=False, num_workers=0)

    model = GitHubModel(
        input_size=X_train.shape[1],
        output_size=y_train.shape[1],
    ).to(device)

    total_params = sum(p.numel() for p in model.parameters())
    print(f"Параметров модели: {total_params:,}")

    criterion = ZeroConstrainedLoss(zero_weight=0.5)
    optimizer = optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=100, eta_min=1e-5)

    best_val_loss  = float("inf")
    patience       = 10
    patience_count = 0
    max_epochs     = 150

    for epoch in range(1, max_epochs + 1):
        train_loss = train_epoch(model, train_loader, optimizer, criterion, device)
        val_loss, val_mae, val_r2 = evaluate(model, val_loader, criterion, device)
        scheduler.step()

        lr_now = optimizer.param_groups[0]["lr"]
        print(
            f"Epoch {epoch:>3}/{max_epochs} | "
            f"train={train_loss:.4f}  val={val_loss:.4f}  "
            f"MAE={val_mae:.4f}  R²={val_r2:.4f}  lr={lr_now:.2e}"
        )

        if val_loss < best_val_loss:
            best_val_loss  = val_loss
            patience_count = 0
            torch.save(model.state_dict(), str(pth_path))
            print("Сохранён лучший checkpoint")
        else:
            patience_count += 1
            if patience_count >= patience:
                print(f"  Early stopping на эпохе {epoch}")
                break

    print("\nЗагружаем лучшую модель для теста…")
    model.load_state_dict(torch.load(str(pth_path), map_location=device))
    test_loss, test_mae, test_r2 = evaluate(model, test_loader, criterion, device)
    print(f"Test loss={test_loss:.4f}  MAE={test_mae:.4f}  R²={test_r2:.4f}")

    print("\nЭкспорт в ONNX…")
    export_onnx(model, onnx_path, input_size=X_train.shape[1])
    verify_onnx(onnx_path, scaler, X_test)

    joblib.dump(scaler, str(scaler_path))
    size_kb = scaler_path.stat().st_size / 1024
    print(f"Scaler сохранён: {scaler_path}  ({size_kb:.1f} KB)")

    print("\nОбучение завершено.")


if __name__ == "__main__":
    main()