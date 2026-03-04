import torch
import numpy as np
from sklearn.metrics import mean_absolute_error, r2_score
from common.Utils.C_ProgressBar import ProgressBar


def train_epoch(model, loader, optimizer, criterion, device) -> float:
    model.train()
    total_loss = 0.0

    progress_bar = ProgressBar(total=len(loader), text="Training")

    for features, targets in loader:
        features = features.to(device)
        targets  = targets.to(device)

        optimizer.zero_grad()
        outputs = model(features)
        loss = criterion(outputs, targets)
        loss.backward()

        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

        optimizer.step()
        total_loss += loss.item()
        progress_bar.update_pd()

    progress_bar.close_pd()
    return total_loss / len(loader)


def evaluate(model, loader, criterion, device):
    model.eval()
    total_loss = 0.0
    all_preds: list  = []
    all_targets: list = []

    with torch.no_grad():
        for features, targets in loader:
            features = features.to(device)
            targets  = targets.to(device)

            outputs = model(features)
            loss = criterion(outputs, targets)
            total_loss += loss.item()

            all_preds.append(outputs.cpu().numpy())
            all_targets.append(targets.cpu().numpy())

    all_preds   = np.concatenate(all_preds)
    all_targets = np.concatenate(all_targets)

    mae = mean_absolute_error(all_targets, all_preds)
    r2  = r2_score(all_targets, all_preds)

    return total_loss / len(loader), mae, r2