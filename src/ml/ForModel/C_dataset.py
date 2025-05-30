import torch
from sklearn.preprocessing import StandardScaler
from torch.utils.data import Dataset
import numpy as np


class GitHubDataset(Dataset):
    def __init__(self, features, targets, transform=None):
        self.scaler = StandardScaler()
        self.features = torch.tensor(
            self.scaler.fit_transform(features.values),
            dtype=torch.float32
        )
        self.targets = torch.tensor(targets.values, dtype=torch.float32)
        self.transform = transform

    def __len__(self):
        return len(self.targets)

    def __getitem__(self, idx):
        sample = (self.features[idx], self.targets[idx])
        if self.transform:
            sample = self.transform(sample)
        return sample

    def get_feature_dim(self):
        return self.features.shape[1]

    def get_target_dim(self):
        return self.targets.shape[1]