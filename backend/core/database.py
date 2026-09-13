from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from backend.core.config import config

engine = create_async_engine(
    config.database_url,
    pool_pre_ping = True
    )

SessionLocal = async_sessionmaker(
    bind = engine,
    autoflush = False,
    autocommit = False,
    expire_on_commit = False,
)

class Base(DeclarativeBase):
    pass

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as db:
        yield db
