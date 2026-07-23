import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class TrainingMetric(Base):
    __tablename__ = "training_metrics"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    round_id = Column(String(36), ForeignKey("training_rounds.id", ondelete="CASCADE"), nullable=False)
    epoch = Column(Integer, default=1)
    loss = Column(Float, nullable=False)
    accuracy = Column(Float, nullable=False)
    val_loss = Column(Float, default=0.0)
    val_accuracy = Column(Float, default=0.0)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    round = relationship("TrainingRound", back_populates="metrics")
