import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

import os
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from GenerationUsers.M_separation_data import separation
from GenerationUsers.C_generation_fake_users import GitHubUserGenerator
from ForModel.C_dataset import GitHubDataset
from ForModel.C_model import GitHubModel
from ForModel.M_education import evaluate, train_epoch

def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    data_dir = Path(os.getenv("DATA_DIR", "data"))
    data_dir.mkdir(parents=True, exist_ok=True)
    path = data_dir / "training.csv"
    model_path = data_dir / "best_model.pth"
    scaler_path = data_dir / "scaler.pth"

    if not Path(path).exists():
        generator = GitHubUserGenerator()
        dff = generator.generate_users()
        generator.save_to_csv(dff, path)

    X_train, y_train, X_val, y_val, X_test, y_test = separation(path)

    train_dataset = GitHubDataset(X_train, y_train, fit_scaler=True)

    scaler = train_dataset.get_scaler()
    val_dataset = GitHubDataset(X_val, y_val, scaler=scaler)
    test_dataset = GitHubDataset(X_test, y_test, scaler=scaler)

    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=64)
    test_loader = DataLoader(test_dataset, batch_size=64)

    model = GitHubModel(input_size=X_train.shape[1],output_size=y_train.shape[1]).to(device)

    criterion = nn.SmoothL1Loss()
    optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-5)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'min', patience=3)
    best_loss = float('inf')

    for epoch in range(100):
        print(f"Epoch {epoch + 1}:")
        
        train_loss = train_epoch(model, train_loader, optimizer, criterion, device)
        val_loss, val_mae, val_r2 = evaluate(model, val_loader, criterion, device)
        scheduler.step(val_loss)

        print(f"  Train Loss: {train_loss:.4f}")
        print(f"  Val Loss: {val_loss:.4f}, MAE: {val_mae:.4f}, R2: {val_r2:.4f}")

        if val_loss < best_loss:
            best_loss = val_loss
            torch.save(model.state_dict(), model_path)
            print("  Saved best model!")

    print("\nTesting best model...")
    model.load_state_dict(torch.load(model_path))
    test_loss, test_mae, test_r2 = evaluate(model, test_loader, criterion, device)
    print(f"Test Loss: {test_loss:.4f}, MAE: {test_mae:.4f}, R2: {test_r2:.4f}")

    torch.save(train_dataset.get_scaler(), scaler_path)

if __name__ == '__main__':
    main()