from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.round_service import RoundService
from app.schemas.round import RoundStartRequest, RoundRead, ModelUpdateSubmission

router = APIRouter(prefix="/rounds", tags=["Federated Rounds"])


@router.get("", response_model=List[RoundRead])
async def get_rounds(db: AsyncSession = Depends(get_db)):
    service = RoundService(db)
    return await service.list_rounds()


@router.get("/{round_id}", response_model=RoundRead)
async def get_round_by_id(round_id: str, db: AsyncSession = Depends(get_db)):
    service = RoundService(db)
    return await service.get_round_by_id(round_id)


@router.post("/start", response_model=RoundRead, status_code=status.HTTP_201_CREATED)
async def start_round(req: RoundStartRequest, db: AsyncSession = Depends(get_db)):
    service = RoundService(db)
    return await service.start_new_round(req)


@router.post("/{round_id}/submit-update", response_model=RoundRead)
async def submit_update(round_id: str, submission: ModelUpdateSubmission, db: AsyncSession = Depends(get_db)):
    service = RoundService(db)
    return await service.submit_local_update(round_id, submission)
