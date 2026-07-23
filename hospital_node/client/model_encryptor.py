import io
import base64
import torch
from typing import Dict


class ModelEncryptor:
    """
    Serializes and encodes PyTorch model state_dict to base64 payload strings for secure API transmission.
    """

    @staticmethod
    def serialize_and_encode(state_dict: Dict[str, torch.Tensor]) -> str:
        buffer = io.BytesIO()
        torch.save(state_dict, buffer)
        raw_bytes = buffer.getvalue()
        return base64.b64encode(raw_bytes).decode("utf-8")

    @staticmethod
    def decode_and_deserialize(b64_str: str) -> Dict[str, torch.Tensor]:
        raw_bytes = base64.b64decode(b64_str)
        buffer = io.BytesIO(raw_bytes)
        return torch.load(buffer, map_location="cpu")
