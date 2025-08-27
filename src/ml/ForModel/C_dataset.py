import torch
from torch.utils.data import Dataset
import numpy as np
from sklearn.preprocessing import StandardScaler

class GitHubDataset(Dataset):
    def __init__(self, features, targets, scaler=None, fit_scaler=False):
        features_np = features.values if hasattr(features, 'values') else features
        targets_np = targets.values if hasattr(targets, 'values') else targets
        if fit_scaler or scaler is None:
            self.scaler = StandardScaler()
            self.features = torch.tensor(
                self.scaler.fit_transform(features_np),
                dtype=torch.float32
            )
        else:
            self.scaler = scaler
            self.features = torch.tensor(
                self.scaler.transform(features_np),
                dtype=torch.float32
            )
        self.targets = torch.tensor(targets_np, dtype=torch.float32)

    def __len__(self):
        return len(self.targets)

    def __getitem__(self, idx):
        return self.features[idx], self.targets[idx]

    def get_scaler(self):
        return self.scaler