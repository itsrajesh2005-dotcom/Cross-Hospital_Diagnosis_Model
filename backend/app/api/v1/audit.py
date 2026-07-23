from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.repositories.audit_repo import AuditRepository
from app.schemas.audit import AuditLogRead

router = APIRouter(prefix="/audit", tags=["Audit & Security"])


@router.get("/logs", response_model=List[AuditLogRead])
async def get_audit_logs(limit: int = 50, db: AsyncSession = Depends(get_db)):
    repo = AuditRepository(db)
    logs = await repo.get_recent_logs(limit=limit)
    return [AuditLogRead.model_validate(l) for l in logs]
