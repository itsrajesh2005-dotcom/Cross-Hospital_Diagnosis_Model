import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


class TrainingRound(Base):
    __tablename__ = "training_rounds"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    round_number = Column(Integer, unique=True, nullable=False, index=True)
    status = Column(String(50), default="IDLE")  # IDLE, SELECTING, TRAINING, AGGREGATING, COMPLETED, FAILED
    target_accuracy = Column(Float, default=0.95)
    min_clients = Column(Integer, default=2)
    participating_clients_count = Column(Integer, default=0)
    current_accuracy = Column(Float, default=0.0)
    current_loss = Column(Float, default=0.0)
    started_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    local_models = relationship("LocalModel", back_populates="round", cascade="all, delete-orphan")
    global_model = relationship("GlobalModel", back_populates="round", uselist=False)
    metrics = relationship("TrainingMetric", back_populates="round", cascade="all, delete-orphan")
