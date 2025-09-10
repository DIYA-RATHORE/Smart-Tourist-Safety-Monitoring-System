# Filename: app/database.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from app.core.config import settings

# For async operations (FastAPI and Async SQLAlchemy)
async_engine = create_async_engine(settings.DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)

Base = declarative_base()

# For Alembic migrations (requires a sync engine)
sync_engine = create_engine(settings.DATABASE_URL.replace("+asyncpg", ""))
SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

async def get_db():
    """
    Dependency to get an async database session.
    """
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()
