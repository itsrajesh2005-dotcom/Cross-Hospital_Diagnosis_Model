import torch
import torch.nn as nn
from app.federated.privacy import DifferentialPrivacyEngine


def test_dp_gradient_clipping():
    dp_engine = DifferentialPrivacyEngine(clip_norm=1.0)
    
    linear = nn.Linear(10, 2)
    x = torch.randn(5, 10)
    out = linear(x).sum() * 100.0  # Large loss to generate gradient norm > 1.0
    out.backward()

    # Verify initial grad norm is clipped to bound 1.0
    total_norm = dp_engine.clip_gradients(list(linear.parameters()))
    assert total_norm > 1.0  # original norm was large

    # Re-calculate clipped norm
    clipped_norm = torch.norm(
        torch.stack([torch.norm(p.grad.detach(), 2) for p in linear.parameters()]), 2
    ).item()
    assert clipped_norm <= 1.0001


def test_dp_privacy_budget():
    dp_engine = DifferentialPrivacyEngine(noise_multiplier=0.05, delta=1e-5)
    eps, delta = dp_engine.compute_privacy_budget(total_steps=100, sample_rate=0.1)
    assert eps > 0
    assert delta == 1e-5
