from pydantic_settings import BaseSettings
from functools import lru_cache
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from redis.asyncio import Redis

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://app:app@postgres:5432/app"
    REDIS_URL: str = "redis://redis:6379/0"

    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()

engine: AsyncEngine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

redis: Redis = Redis.from_url(settings.REDIS_URL, decode_responses=True)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

async def get_redis() -> Redis:
    return redis
