import base64
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.repositories.round_repo import TrainingRoundRepository
from app.repositories.hospital_repo import HospitalRepository
from app.repositories.model_repo import LocalModelRepository
from app.federated.client_selector import ClientSelectionStrategy
from app.services.aggregation_service import AggregationService
from app.core.exceptions import EntityNotFoundException, DuplicateResourceException
from app.core.s3 import storage_manager
from app.models.round import TrainingRound
from app.models.model_registry import LocalModel
from app.models.audit import AuditLog
from app.schemas.round import RoundStartRequest, RoundRead, ModelUpdateSubmission


class RoundService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.round_repo = TrainingRoundRepository(db)
        self.hospital_repo = HospitalRepository(db)
        self.local_model_repo = LocalModelRepository(db)
        self.aggregation_service = AggregationService(db)

    async def list_rounds(self) -> List[RoundRead]:
        rounds = await self.round_repo.get_all()
        return [RoundRead.model_validate(r) for r in rounds]

    async def get_round_by_id(self, round_id: str) -> RoundRead:
        r = await self.round_repo.get_by_id(round_id)
        if not r:
            raise EntityNotFoundException("TrainingRound", round_id)
        return RoundRead.model_validate(r)

    async def start_new_round(self, req: RoundStartRequest) -> RoundRead:
        active_round = await self.round_repo.get_active_round()
        if active_round:
            raise DuplicateResourceException(f"Round #{active_round.round_number} is currently in progress ({active_round.status}).")

        latest_round = await self.round_repo.get_latest_round()
        next_number = (latest_round.round_number + 1) if latest_round else 1

        hospitals = await self.hospital_repo.get_all()
        selected_clients = ClientSelectionStrategy.select_clients(hospitals, req.min_clients)

        new_round = TrainingRound(
            round_number=next_number,
            status="TRAINING",
            target_accuracy=req.target_accuracy,
            min_clients=req.min_clients,
            participating_clients_count=len(selected_clients),
            current_accuracy=latest_round.current_accuracy if latest_round else 0.70,
            current_loss=latest_round.current_loss if latest_round else 0.45,
            started_at=datetime.now(timezone.utc)
        )

        created = await self.round_repo.create(new_round)

        # Audit Log
        audit = AuditLog(
            action="ROUND_STARTED",
            resource_type="TRAINING_ROUND",
            resource_id=created.id,
            details={"round_number": next_number, "clients_count": len(selected_clients)}
        )
        self.db.add(audit)
        await self.db.commit()

        return RoundRead.model_validate(created)

    async def submit_local_update(self, round_id: str, submission: ModelUpdateSubmission) -> RoundRead:
        round_obj = await self.round_repo.get_by_id(round_id)
        if not round_obj:
            raise EntityNotFoundException("TrainingRound", round_id)

        hospital = await self.hospital_repo.get_by_code(submission.hospital_code)
        if not hospital:
            raise EntityNotFoundException("Hospital", submission.hospital_code)

        # Decode base64 model weights and save to storage
        raw_weights = base64.b64decode(submission.weights_b64)
        s3_key = f"local_models/round_{round_obj.round_number}/{hospital.code}_weights.pt"
        s3_path = storage_manager.upload_bytes(s3_key, raw_weights)

        # Save LocalModel record
        local_model = LocalModel(
            round_id=round_obj.id,
            hospital_id=hospital.id,
            s3_storage_path=s3_path,
            sample_count=submission.sample_count,
            local_loss=submission.local_loss,
            local_accuracy=submission.local_accuracy,
            dp_epsilon=submission.dp_epsilon,
            dp_delta=submission.dp_delta,
            submitted_at=datetime.now(timezone.utc)
        )
        self.db.add(local_model)
        await self.db.commit()

        # Check if enough clients submitted updates to aggregate
        submitted_models = await self.local_model_repo.get_models_for_round(round_obj.id)
        
        if len(submitted_models) >= round_obj.min_clients and round_obj.status == "TRAINING":
            round_obj.status = "AGGREGATING"
            await self.round_repo.update(round_obj)

            # Trigger Aggregation
            global_model = await self.aggregation_service.aggregate_round(round_obj)

            round_obj.status = "COMPLETED"
            round_obj.current_accuracy = global_model.accuracy
            round_obj.current_loss = global_model.loss
            round_obj.completed_at = datetime.now(timezone.utc)
            await self.round_repo.update(round_obj)

        return RoundRead.model_validate(round_obj)
