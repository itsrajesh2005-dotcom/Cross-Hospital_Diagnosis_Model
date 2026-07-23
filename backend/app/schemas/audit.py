from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel


class AuditLogRead(BaseModel):
    id: str
    user_id: Optional[str] = None
    action: str
    resource_type: str
    resource_id: Optional[str] = None
    ip_address: str
    details: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True
