import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    hospital_id = Column(String(36), ForeignKey("hospitals.id", ondelete="SET NULL"), nullable=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), default="HOSPITAL_ADMIN")  # SYSTEM_ADMIN, HOSPITAL_ADMIN, RESEARCHER, AUDITOR
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    hospital = relationship("Hospital", back_populates="users")
    audit_logs = relationship("AuditLog", back_populates="user")
