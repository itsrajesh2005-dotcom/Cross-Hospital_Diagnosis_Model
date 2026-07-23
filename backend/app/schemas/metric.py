from datetime import datetime
from pydantic import BaseModel


class MetricRead(BaseModel):
    id: str
    round_id: str
    epoch: int
    loss: float
    accuracy: float
    val_loss: float
    val_accuracy: float
    timestamp: datetime

    class Config:
        from_attributes = True
