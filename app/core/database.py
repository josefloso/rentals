# COMPLETELY REPLACE the existing file with:
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool
from .config import settings

# MUST use asyncpg and NullPool for NeonDB
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL.replace(
    "postgresql://", "postgresql+asyncpg://"
)

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
    poolclass=NullPool  # Critical for serverless DBs
)

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()