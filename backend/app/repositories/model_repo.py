from typing import Optional, List
from sqlalchemy.future import select
from app.repositories.base import BaseRepository
from app.models.model_registry import GlobalModel, LocalModel


class GlobalModelRepository(BaseRepository[GlobalModel]):
    def __init__(self, db):
        super().__init__(GlobalModel, db)

    async def get_latest_version(self) -> Optional[GlobalModel]:
        result = await self.db.execute(
            select(GlobalModel).order_by(GlobalModel.created_at.desc())
        )
        return result.scalars().first()

    async def get_by_version(self, version: str) -> Optional[GlobalModel]:
        result = await self.db.execute(
            select(GlobalModel).filter(GlobalModel.version == version)
        )
        return result.scalars().first()


class LocalModelRepository(BaseRepository[LocalModel]):
    def __init__(self, db):
        super().__init__(LocalModel, db)

    async def get_models_for_round(self, round_id: str) -> List[LocalModel]:
        result = await self.db.execute(
            select(LocalModel).filter(LocalModel.round_id == round_id)
        )
        return list(result.scalars().all())
