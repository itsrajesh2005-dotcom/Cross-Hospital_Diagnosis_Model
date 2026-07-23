from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.report_service import ReportService
from app.schemas.report import ConsortiumReport

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/summary", response_model=ConsortiumReport)
async def get_consortium_report(db: AsyncSession = Depends(get_db)):
    service = ReportService(db)
    return await service.generate_consortium_report()
