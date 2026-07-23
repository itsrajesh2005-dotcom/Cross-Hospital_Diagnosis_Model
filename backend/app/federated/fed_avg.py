import io
import torch
import logging
from typing import List, Dict, Any, Tuple
from app.federated.privacy import DifferentialPrivacyEngine

logger = logging.getLogger(__name__)


class FederatedAvgAggregator:
    """
    Federated Averaging (FedAvg) implementation using PyTorch tensors.
    Aggregates local model updates weighted by dataset size:
    
        theta_global = sum_{k=1}^K (n_k / N) * theta_k
    """

    @staticmethod
    def bytes_to_state_dict(model_bytes: bytes) -> Dict[str, torch.Tensor]:
        buffer = io.BytesIO(model_bytes)
        return torch.load(buffer, map_location="cpu")

    @staticmethod
    def state_dict_to_bytes(state_dict: Dict[str, torch.Tensor]) -> bytes:
        buffer = io.BytesIO()
        torch.save(state_dict, buffer)
        return buffer.getvalue()

    @classmethod
    def aggregate(
        cls,
        client_updates: List[Tuple[Dict[str, torch.Tensor], int]],
        apply_dp: bool = True,
        clip_norm: float = 1.0,
        noise_multiplier: float = 0.1
    ) -> Dict[str, torch.Tensor]:
        """
        :param client_updates: List of tuples containing (state_dict, sample_count)
        :param apply_dp: Whether server-side DP noise verification is applied
        """
        if not client_updates:
            raise ValueError("Cannot perform FedAvg aggregation with empty client updates list.")

        total_samples = sum(sample_count for _, sample_count in client_updates)
        if total_samples <= 0:
            raise ValueError("Total dataset samples across participating clients must be > 0.")

        logger.info(f"Aggregating model weights from {len(client_updates)} clients over {total_samples} total diagnostic samples.")

        # Initialize global state dict with zeroed tensors matching the shape of the first client update
        first_weights, _ = client_updates[0]
        aggregated_weights: Dict[str, torch.Tensor] = {}

        for key, tensor in first_weights.items():
            if tensor.is_floating_point():
                aggregated_weights[key] = torch.zeros_like(tensor, dtype=torch.float32)
            else:
                aggregated_weights[key] = torch.zeros_like(tensor)

        # Weighted summation
        for client_weights, sample_count in client_updates:
            weight_factor = sample_count / total_samples
            for key, tensor in client_weights.items():
                if tensor.is_floating_point():
                    aggregated_weights[key] += (tensor.to(torch.float32) * weight_factor)
                else:
                    # Non-floating point tensors (e.g. num_batches_tracked) take mode/first value
                    aggregated_weights[key] = tensor

        # Optional Differential Privacy noise addition on server side aggregation
        if apply_dp:
            dp_engine = DifferentialPrivacyEngine(clip_norm=clip_norm, noise_multiplier=noise_multiplier)
            aggregated_weights = dp_engine.add_gaussian_noise_to_weights(aggregated_weights)

        return aggregated_weights
