from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from .settings import settings
engine = create_async_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)
