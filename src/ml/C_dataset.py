import torch
from torch.utils.data import Dataset
import numpy as np


class GitHubDataset(Dataset):
    def __init__(self, features, targets, transform=None):
        self.features = torch.tensor(features.values if hasattr(features, 'values')
                                     else features.astype(np.float32), dtype=torch.float32)
        self.targets = torch.tensor(targets.values if hasattr(targets, 'values')
                                    else targets.astype(np.float32), dtype=torch.float32)
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