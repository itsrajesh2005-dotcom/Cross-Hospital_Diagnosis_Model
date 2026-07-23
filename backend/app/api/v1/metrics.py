from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.metric import TrainingMetric
from app.schemas.metric import MetricRead

router = APIRouter(prefix="/metrics", tags=["Metrics"])


@router.get("/training", response_model=List[MetricRead])
async def get_training_metrics(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TrainingMetric).order_by(TrainingMetric.timestamp.asc()))
    metrics = result.scalars().all()
    return [MetricRead.model_validate(m) for m in metrics]
