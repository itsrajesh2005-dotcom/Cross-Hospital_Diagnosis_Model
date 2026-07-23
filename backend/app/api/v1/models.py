from typing import List
from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.repositories.model_repo import GlobalModelRepository
from app.core.s3 import storage_manager
from app.core.exceptions import EntityNotFoundException
from app.schemas.model_registry import GlobalModelRead

router = APIRouter(prefix="/models", tags=["Model Registry"])


@router.get("/global", response_model=List[GlobalModelRead])
async def list_global_models(db: AsyncSession = Depends(get_db)):
    repo = GlobalModelRepository(db)
    models = await repo.get_all()
    return [GlobalModelRead.model_validate(m) for m in models]


@router.get("/global/latest", response_model=GlobalModelRead)
async def get_latest_global_model(db: AsyncSession = Depends(get_db)):
    repo = GlobalModelRepository(db)
    m = await repo.get_latest_version()
    if not m:
        raise EntityNotFoundException("GlobalModel", "latest")
    return GlobalModelRead.model_validate(m)


@router.get("/{model_id}/download")
async def download_model_weights(model_id: str, db: AsyncSession = Depends(get_db)):
    repo = GlobalModelRepository(db)
    m = await repo.get_by_id(model_id)
    if not m:
        raise EntityNotFoundException("GlobalModel", model_id)

    raw_bytes = storage_manager.download_bytes(m.s3_storage_path)
    return Response(
        content=raw_bytes,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename=global_model_{m.version}.pt"}
    )
