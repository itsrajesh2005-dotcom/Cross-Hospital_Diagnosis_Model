import torch
from torch.utils.data import Dataset, DataLoader


class DiagnosticDataset(Dataset):
    """
    Synthetic diagnostic medical dataset simulator (e.g. Chest X-Ray diagnostic features).
    Simulates local hospital patient data that stays strictly on-premise.
    """

    def __init__(self, num_samples: int = 1000, num_features: int = 64, num_classes: int = 2):
        self.num_samples = num_samples
        # Fixed generator seed per dataset size for consistent synthetic features
        g = torch.Generator().manual_seed(num_samples)
        self.features = torch.randn(num_samples, num_features, generator=g)
        # Binary target: 0 = Normal, 1 = Diagnostic Abnormality / Pneumonia
        self.targets = torch.randint(0, num_classes, (num_samples,), generator=g)

    def __len__(self):
        return self.num_samples

    def __getitem__(self, idx):
        return self.features[idx], self.targets[idx]


def get_diagnostic_dataloader(num_samples: int = 1000, batch_size: int = 32) -> DataLoader:
    dataset = DiagnosticDataset(num_samples=num_samples)
    return DataLoader(dataset, batch_size=batch_size, shuffle=True)
