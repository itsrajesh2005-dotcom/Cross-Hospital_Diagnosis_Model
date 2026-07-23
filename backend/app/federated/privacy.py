import math
import torch
import logging
from typing import Dict

logger = logging.getLogger(__name__)


class DifferentialPrivacyEngine:
    """
    Differential Privacy (DP-SGD) utility for gradient clipping, noise injection,
    and privacy budget budget tracking (Renyi Differential Privacy / Moments Accountant approximation).
    """

    def __init__(self, clip_norm: float = 1.0, noise_multiplier: float = 0.1, delta: float = 1e-5):
        self.clip_norm = clip_norm
        self.noise_multiplier = noise_multiplier
        self.delta = delta

    def clip_gradients(self, parameters: list[torch.Tensor]) -> float:
        """Clips parameter gradients in-place to L2 norm bound."""
        total_norm = torch.norm(
            torch.stack([torch.norm(p.grad.detach(), 2) for p in parameters if p.grad is not None]), 2
        ).item()

        clip_coef = self.clip_norm / (total_norm + 1e-6)
        if clip_coef < 1.0:
            for p in parameters:
                if p.grad is not None:
                    p.grad.detach().mul_(clip_coef)
        return total_norm

    def add_gaussian_noise_to_weights(self, state_dict: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:
        """Adds calibrated Gaussian noise to model weights/gradients."""
        noisy_dict = {}
        sigma = self.noise_multiplier * self.clip_norm

        for key, tensor in state_dict.items():
            if tensor.is_floating_point():
                noise = torch.normal(
                    mean=0.0,
                    std=sigma,
                    size=tensor.size(),
                    device=tensor.device,
                    dtype=tensor.dtype
                )
                noisy_dict[key] = tensor + noise
            else:
                noisy_dict[key] = tensor
        return noisy_dict

    def compute_privacy_budget(self, total_steps: int, sample_rate: float) -> tuple[float, float]:
        """
        Calculates an approximate privacy budget (Epsilon) given noise multiplier, total steps, and sampling rate.
        Ref: Abadi et al., "Deep Learning with Differential Privacy"
        """
        if self.noise_multiplier == 0:
            return float("inf"), self.delta

        # Basic Moment Accountant analytic upper bound approximation
        q = sample_rate
        steps = total_steps
        sigma = self.noise_multiplier

        eps = q * math.sqrt(steps * math.log(1 / self.delta)) / sigma
        return round(eps, 4), self.delta
