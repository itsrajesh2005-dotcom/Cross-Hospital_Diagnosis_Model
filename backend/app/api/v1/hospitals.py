from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.hospital_service import HospitalService
from app.schemas.hospital import (
    HospitalCreate,
    HospitalRead,
    HospitalHeartbeat,
    HospitalRegisterNodeResponse,
)

router = APIRouter(prefix="/hospitals", tags=["Hospital Management"])


@router.get("", response_model=List[HospitalRead])
async def get_hospitals(db: AsyncSession = Depends(get_db)):
    service = HospitalService(db)
    return await service.list_hospitals()


@router.get("/{hospital_id}", response_model=HospitalRead)
async def get_hospital_by_id(hospital_id: str, db: AsyncSession = Depends(get_db)):
    service = HospitalService(db)
    return await service.get_hospital_by_id(hospital_id)


@router.post("/register-node", response_model=HospitalRegisterNodeResponse, status_code=status.HTTP_201_CREATED)
async def register_hospital_node(payload: HospitalCreate, db: AsyncSession = Depends(get_db)):
    service = HospitalService(db)
    return await service.register_hospital_node(payload)


@router.post("/{code}/heartbeat", response_model=HospitalRead)
async def hospital_heartbeat(code: str, payload: HospitalHeartbeat, db: AsyncSession = Depends(get_db)):
    service = HospitalService(db)
    return await service.record_heartbeat(code, payload.dataset_sample_count)
