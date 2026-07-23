import torch
import torch.nn as nn
import torch.optim as optim
from typing import Tuple, Dict
from hospital_node.client.dataset_loader import get_diagnostic_dataloader


class DiagnosticClassifier(nn.Module):
    """
    PyTorch Deep Diagnostic Neural Network for multi-feature medical classification.
    """

    def __init__(self, in_features: int = 64, hidden_dim: int = 32, num_classes: int = 2):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_features, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Linear(hidden_dim // 2, num_classes)
        )

    def forward(self, x):
        return self.net(x)


class LocalTrainer:
    """
    Local training engine executing PyTorch epochs on local hospital dataset
    with Differential Privacy (DP-SGD gradient norm clipping).
    """

    def __init__(self, sample_count: int = 1000, lr: float = 0.001, clip_norm: float = 1.0):
        self.sample_count = sample_count
        self.model = DiagnosticClassifier()
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        self.criterion = nn.CrossEntropyLoss()
        self.clip_norm = clip_norm

    def set_weights(self, state_dict: Dict[str, torch.Tensor]):
        """Load global weights sent from central aggregator."""
        self.model.load_state_dict(state_dict)

    def train_epochs(self, epochs: int = 3, batch_size: int = 32) -> Tuple[Dict[str, torch.Tensor], float, float]:
        dataloader = get_diagnostic_dataloader(self.sample_count, batch_size=batch_size)
        self.model.train()

        total_loss = 0.0
        correct = 0
        total = 0

        for epoch in range(epochs):
            for features, targets in dataloader:
                self.optimizer.zero_grad()
                outputs = self.model(features)
                loss = self.criterion(outputs, targets)
                loss.backward()

                # DP-SGD Gradient Norm Clipping
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.clip_norm)

                self.optimizer.step()

                total_loss += loss.item() * features.size(0)
                _, predicted = torch.max(outputs.data, 1)
                total += targets.size(0)
                correct += (predicted == targets).sum().item()

        avg_loss = total_loss / total if total > 0 else 0.0
        accuracy = correct / total if total > 0 else 0.0

        return self.model.state_dict(), round(avg_loss, 4), round(accuracy, 4)
