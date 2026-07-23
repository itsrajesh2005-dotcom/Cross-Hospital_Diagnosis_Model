from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings

db_uri = settings.SQLALCHEMY_DATABASE_URI or "sqlite+aiosqlite:///./sql_app.db"
is_sqlite = db_uri.startswith("sqlite")

engine_kwargs = {"echo": False, "future": True}
if not is_sqlite:
    engine_kwargs["pool_pre_ping"] = True

engine = create_async_engine(db_uri, **engine_kwargs)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
