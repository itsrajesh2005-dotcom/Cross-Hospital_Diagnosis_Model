from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class RoundStartRequest(BaseModel):
    min_clients: int = 2
    target_accuracy: float = 0.95


class RoundRead(BaseModel):
    id: str
    round_number: int
    status: str
    target_accuracy: float
    min_clients: int
    participating_clients_count: int
    current_accuracy: float
    current_loss: float
    started_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ModelUpdateSubmission(BaseModel):
    hospital_code: str
    sample_count: int
    local_loss: float
    local_accuracy: float
    dp_epsilon: float = 0.5
    dp_delta: float = 1e-5
    weights_b64: str  # Base64-encoded PyTorch weights state dict
