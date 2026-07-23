from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.report_service import ReportService
from app.schemas.report import DashboardSummary

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary", response_model=DashboardSummary)
async def get_dashboard_summary(db: AsyncSession = Depends(get_db)):
    service = ReportService(db)
    return await service.get_dashboard_summary()
