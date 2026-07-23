import secrets
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.hospital_repo import HospitalRepository
from app.core.security import get_password_hash
from app.core.exceptions import DuplicateResourceException, EntityNotFoundException
from app.models.hospital import Hospital
from app.schemas.hospital import HospitalCreate, HospitalUpdate, HospitalRead, HospitalRegisterNodeResponse


class HospitalService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = HospitalRepository(db)

    async def list_hospitals(self) -> List[HospitalRead]:
        hospitals = await self.repo.get_all()
        return [HospitalRead.model_validate(h) for h in hospitals]

    async def get_hospital_by_id(self, hospital_id: str) -> HospitalRead:
        h = await self.repo.get_by_id(hospital_id)
        if not h:
            raise EntityNotFoundException("Hospital", hospital_id)
        return HospitalRead.model_validate(h)

    async def register_hospital_node(self, payload: HospitalCreate) -> HospitalRegisterNodeResponse:
        existing = await self.repo.get_by_code(payload.code)
        if existing:
            raise DuplicateResourceException(f"Hospital with code '{payload.code}' is already registered.")

        raw_api_key = f"hkey_{secrets.token_urlsafe(24)}"
        api_key_hash = get_password_hash(raw_api_key)

        hospital = Hospital(
            name=payload.name,
            code=payload.code,
            endpoint_url=payload.endpoint_url,
            dataset_sample_count=payload.dataset_sample_count,
            location=payload.location or "Consortium Node",
            api_key_hash=api_key_hash,
            status="ACTIVE",
            last_heartbeat=datetime.now(timezone.utc)
        )

        created = await self.repo.create(hospital)
        return HospitalRegisterNodeResponse(
            hospital=HospitalRead.model_validate(created),
            api_key=raw_api_key
        )

    async def record_heartbeat(self, code: str, sample_count: Optional[int] = None) -> HospitalRead:
        hospital = await self.repo.get_by_code(code)
        if not hospital:
            raise EntityNotFoundException("Hospital", code)

        hospital.status = "ACTIVE"
        hospital.last_heartbeat = datetime.now(timezone.utc)
        if sample_count is not None:
            hospital.dataset_sample_count = sample_count

        updated = await self.repo.update(hospital)
        return HospitalRead.model_validate(updated)
