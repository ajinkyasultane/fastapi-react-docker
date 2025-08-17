from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from .db import engine
from .deps import db_dep, redis_dep
from .models import Base
from redis.asyncio import Redis

app = FastAPI(title="FastAPI + React Scaffold")

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/health")
async def health(db: AsyncSession = Depends(db_dep), r: Redis = Depends(redis_dep)):
    result = await db.execute(text("SELECT 1"))
    db_ok = result.scalar() == 1
    pong = await r.ping()
    return {"status": "ok", "postgres": db_ok, "redis": pong}

@app.get("/api/widgets")
async def list_widgets(db: AsyncSession = Depends(db_dep)):
    rows = (await db.execute(text("SELECT id, name FROM widgets ORDER BY id"))).mappings().all()
    return {"items": [dict(row) for row in rows]}

@app.post("/api/widgets")
async def add_widget(name: str, db: AsyncSession = Depends(db_dep)):
    await db.execute(text("INSERT INTO widgets(name) VALUES (:name)"), {"name": name})
    await db.commit()
    return {"ok": True}
