from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from .db import get_db, get_redis

async def db_dep(session: AsyncSession = Depends(get_db)) -> AsyncSession:
    return session

async def redis_dep(client: Redis = Depends(get_redis)) -> Redis:
    return client
