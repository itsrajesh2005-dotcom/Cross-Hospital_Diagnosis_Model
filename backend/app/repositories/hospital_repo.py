from typing import Optional, List
from sqlalchemy.future import select
from app.repositories.base import BaseRepository
from app.models.hospital import Hospital


class HospitalRepository(BaseRepository[Hospital]):
    def __init__(self, db):
        super().__init__(Hospital, db)

    async def get_by_code(self, code: str) -> Optional[Hospital]:
        result = await self.db.execute(select(Hospital).filter(Hospital.code == code))
        return result.scalars().first()

    async def get_active_hospitals(self) -> List[Hospital]:
        result = await self.db.execute(select(Hospital).filter(Hospital.status == "ACTIVE"))
        return list(result.scalars().all())
