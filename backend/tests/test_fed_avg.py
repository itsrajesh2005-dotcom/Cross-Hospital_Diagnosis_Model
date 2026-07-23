import torch
import pytest
from app.federated.fed_avg import FederatedAvgAggregator


def test_fed_avg_mathematical_correctness():
    # Model with 2 parameters: [w1, w2]
    # Client 1: weights = [2.0, 4.0], sample_count = 100
    # Client 2: weights = [4.0, 8.0], sample_count = 300
    # Total samples = 400
    # Expected weighted avg:
    # w1 = (2.0 * 100 + 4.0 * 300) / 400 = (200 + 1200) / 400 = 3.5
    # w2 = (4.0 * 100 + 8.0 * 300) / 400 = (400 + 2400) / 400 = 7.0

    c1_state = {"weight": torch.tensor([2.0, 4.0], dtype=torch.float32)}
    c2_state = {"weight": torch.tensor([4.0, 8.0], dtype=torch.float32)}

    updates = [
        (c1_state, 100),
        (c2_state, 300),
    ]

    aggregated = FederatedAvgAggregator.aggregate(updates, apply_dp=False)

    assert torch.isclose(aggregated["weight"][0], torch.tensor(3.5), atol=1e-4)
    assert torch.isclose(aggregated["weight"][1], torch.tensor(7.0), atol=1e-4)


def test_fed_avg_empty_updates_raises_error():
    with pytest.raises(ValueError, match="Cannot perform FedAvg aggregation"):
        FederatedAvgAggregator.aggregate([])
