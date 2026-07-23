from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.hospitals import router as hospitals_router
from app.api.v1.rounds import router as rounds_router
from app.api.v1.models import router as models_router
from app.api.v1.metrics import router as metrics_router
from app.api.v1.audit import router as audit_router
from app.api.v1.reports import router as reports_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.websocket import router as ws_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(hospitals_router)
api_router.include_router(rounds_router)
api_router.include_router(models_router)
api_router.include_router(metrics_router)
api_router.include_router(audit_router)
api_router.include_router(reports_router)
api_router.include_router(dashboard_router)
api_router.include_router(ws_router)
