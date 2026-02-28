import torch
import torch.nn as nn


class ZeroConstrainedLoss(nn.Module):
    def __init__(self, zero_weight: float = 0.5):
        super().__init__()
        self.base = nn.SmoothL1Loss()
        self.zero_weight = zero_weight

    def forward(self, outputs: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        base_loss = self.base(outputs, targets)

        zero_mask = (targets == 0.0).float()
        zero_penalty = (outputs * zero_mask).pow(2).mean()

        return base_loss + self.zero_weight * zero_penalty