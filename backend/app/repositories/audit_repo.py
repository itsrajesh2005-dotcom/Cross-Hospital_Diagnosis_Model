from typing import List
from sqlalchemy.future import select
from app.repositories.base import BaseRepository
from app.models.audit import AuditLog


class AuditRepository(BaseRepository[AuditLog]):
    def __init__(self, db):
        super().__init__(AuditLog, db)

    async def get_recent_logs(self, limit: int = 50) -> List[AuditLog]:
        result = await self.db.execute(
            select(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit)
        )
        return list(result.scalars().all())
