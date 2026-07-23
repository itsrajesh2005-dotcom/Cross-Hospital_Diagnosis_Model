from typing import Optional, List
from sqlalchemy.future import select
from sqlalchemy import func
from app.repositories.base import BaseRepository
from app.models.round import TrainingRound


class TrainingRoundRepository(BaseRepository[TrainingRound]):
    def __init__(self, db):
        super().__init__(TrainingRound, db)

    async def get_latest_round(self) -> Optional[TrainingRound]:
        result = await self.db.execute(
            select(TrainingRound).order_by(TrainingRound.round_number.desc())
        )
        return result.scalars().first()

    async def get_by_round_number(self, round_number: int) -> Optional[TrainingRound]:
        result = await self.db.execute(
            select(TrainingRound).filter(TrainingRound.round_number == round_number)
        )
        return result.scalars().first()

    async def get_active_round(self) -> Optional[TrainingRound]:
        result = await self.db.execute(
            select(TrainingRound).filter(TrainingRound.status.in_(["SELECTING", "TRAINING", "AGGREGATING"]))
        )
        return result.scalars().first()
