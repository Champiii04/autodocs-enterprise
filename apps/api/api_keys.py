import os, secrets
from fastapi import Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .db import SessionLocal
from .models import ApiKey, Project

async def get_db():
    async with SessionLocal() as s: yield s

def generate_api_key() -> str:
    return secrets.token_urlsafe(40)

async def require_api_key(x_api_key: str | None = Header(default=None), db: AsyncSession = Depends(get_db)) -> Project:
    if not x_api_key:
        raise HTTPException(401, "X-API-Key requerido")
    ap = (await db.execute(select(ApiKey).where(ApiKey.key == x_api_key, ApiKey.active == True))).scalar_one_or_none()
    if not ap:
        raise HTTPException(403, "API key no válida")
    proj = (await db.execute(select(Project).where(Project.id == ap.project_id))).scalar_one()
    return proj
