from datetime import datetime
from typing import Optional
from pydantic import BaseModel, HttpUrl


class HospitalCreate(BaseModel):
    name: str
    code: str
    endpoint_url: Optional[str] = None
    dataset_sample_count: int = 1000
    location: Optional[str] = "Consortium Edge"


class HospitalUpdate(BaseModel):
    name: Optional[str] = None
    endpoint_url: Optional[str] = None
    dataset_sample_count: Optional[int] = None
    status: Optional[str] = None
    location: Optional[str] = None


class HospitalHeartbeat(BaseModel):
    status: str = "ACTIVE"
    dataset_sample_count: Optional[int] = None


class HospitalRead(BaseModel):
    id: str
    name: str
    code: str
    endpoint_url: Optional[str] = None
    dataset_sample_count: int
    status: str
    last_heartbeat: datetime
    location: str
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True


class HospitalRegisterNodeResponse(BaseModel):
    hospital: HospitalRead
    api_key: str
