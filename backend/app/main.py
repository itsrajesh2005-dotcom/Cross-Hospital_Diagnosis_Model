from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
try:
    from prometheus_fastapi_instrumentator import Instrumentator
    HAS_PROMETHEUS = True
except ImportError:
    HAS_PROMETHEUS = False

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.database import engine, Base
from app.api.v1.router import api_router

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Auto-create PostgreSQL database if it does not exist
    if settings.SQLALCHEMY_DATABASE_URI.startswith("postgresql"):
        try:
            import asyncpg
            conn = await asyncpg.connect(
                user=settings.POSTGRES_USER,
                password=settings.POSTGRES_PASSWORD,
                host=settings.POSTGRES_SERVER,
                port=settings.POSTGRES_PORT,
                database="postgres"
            )
            try:
                exists = await conn.fetchval("SELECT 1 FROM pg_database WHERE datname = $1", settings.POSTGRES_DB)
                if not exists:
                    await conn.execute(f'CREATE DATABASE "{settings.POSTGRES_DB}"')
            finally:
                await conn.close()
        except Exception:
            pass

    # Startup: Create tables if they do not exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Prometheus Monitoring Instrumentator (if installed)
if HAS_PROMETHEUS:
    Instrumentator().instrument(app).expose(app)


@app.get("/")
async def root():
    return {
        "platform": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "ONLINE",
        "docs_url": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "HEALTHY"}
