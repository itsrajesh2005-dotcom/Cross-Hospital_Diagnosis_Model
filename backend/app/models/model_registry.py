import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class GlobalModel(Base):
    __tablename__ = "global_models"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    round_id = Column(String(36), ForeignKey("training_rounds.id", ondelete="CASCADE"), nullable=False)
    version = Column(String(50), unique=True, nullable=False, index=True)
    s3_storage_path = Column(Text, nullable=False)
    accuracy = Column(Float, default=0.0)
    loss = Column(Float, default=0.0)
    f1_score = Column(Float, default=0.0)
    metrics_summary = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    round = relationship("TrainingRound", back_populates="global_model")


class LocalModel(Base):
    __tablename__ = "local_models"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    round_id = Column(String(36), ForeignKey("training_rounds.id", ondelete="CASCADE"), nullable=False)
    hospital_id = Column(String(36), ForeignKey("hospitals.id", ondelete="CASCADE"), nullable=False)
    s3_storage_path = Column(Text, nullable=False)
    sample_count = Column(Integer, nullable=False, default=100)
    local_loss = Column(Float, default=0.0)
    local_accuracy = Column(Float, default=0.0)
    dp_epsilon = Column(Float, default=0.5)
    dp_delta = Column(Float, default=1e-5)
    submitted_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    round = relationship("TrainingRound", back_populates="local_models")
    hospital = relationship("Hospital", back_populates="local_models")
