import torch
from sklearn.metrics import mean_absolute_error, r2_score
import numpy as np

from tqdm import tqdm 

def train_epoch(model, loader, optimizer, criterion, device):
    model.train()
    total_loss = 0.0
    
    progress_bar = tqdm(
        enumerate(loader),
        total=len(loader),
        desc="Training",
        leave=True,
        ncols=80,                
        colour="green",          
    )
    
    for batch_idx, (features, targets) in progress_bar:
        features, targets = features.to(device), targets.to(device)

        optimizer.zero_grad()
        outputs = model(features)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
        
    return total_loss / len(loader)


def evaluate(model, loader, criterion, device):
    model.eval()
    total_loss = 0.0
    all_preds = []
    all_targets = []

    with torch.no_grad():
        for features, targets in loader:
            features, targets = features.to(device), targets.to(device)
            outputs = model(features)

            loss = criterion(outputs, targets)
            total_loss += loss.item()

            all_preds.append(outputs.cpu().numpy())
            all_targets.append(targets.cpu().numpy())

    all_preds = np.concatenate(all_preds)
    all_targets = np.concatenate(all_targets)

    mae = mean_absolute_error(all_targets, all_preds)
    r2 = r2_score(all_targets, all_preds)

    return total_loss / len(loader), mae, r2