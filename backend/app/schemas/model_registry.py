from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel


class GlobalModelRead(BaseModel):
    id: str
    round_id: str
    version: str
    s3_storage_path: str
    accuracy: float
    loss: float
    f1_score: float
    metrics_summary: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True


class LocalModelRead(BaseModel):
    id: str
    round_id: str
    hospital_id: str
    s3_storage_path: str
    sample_count: int
    local_loss: float
    local_accuracy: float
    dp_epsilon: float
    dp_delta: float
    submitted_at: datetime

    class Config:
        from_attributes = True
