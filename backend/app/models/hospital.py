import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class Hospital(Base):
    __tablename__ = "hospitals"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    api_key_hash = Column(String(255), nullable=False)
    endpoint_url = Column(String(255), nullable=True)
    dataset_sample_count = Column(Integer, default=1000)
    status = Column(String(50), default="ACTIVE")  # ACTIVE, OFFLINE, TRAINING, ERROR
    last_heartbeat = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    location = Column(String(255), default="Consortium Edge")
    is_verified = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    users = relationship("User", back_populates="hospital", cascade="all, delete-orphan")
    local_models = relationship("LocalModel", back_populates="hospital", cascade="all, delete-orphan")
