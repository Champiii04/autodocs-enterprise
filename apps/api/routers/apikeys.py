from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..auth import require_roles
from ..db import SessionLocal
from ..models import Project, ApiKey
from ..api_keys import generate_api_key

router = APIRouter()
async def get_db():
    async with SessionLocal() as s: yield s

class ProjectIn(BaseModel):
    name: str

@router.post("/projects", dependencies=[Depends(require_roles('admin'))])
async def create_project(payload: ProjectIn, db: AsyncSession = Depends(get_db)):
    p = Project(name=payload.name); db.add(p); await db.commit(); await db.refresh(p)
    return {"id": p.id, "name": p.name}

@router.post("/projects/{project_id}/keys", dependencies=[Depends(require_roles('admin'))])
async def create_key(project_id: int, db: AsyncSession = Depends(get_db)):
    key = generate_api_key()
    ak = ApiKey(project_id=project_id, key=key, active=True); db.add(ak); await db.commit(); await db.refresh(ak)
    return {"id": ak.id, "key": ak.key, "active": ak.active}

@router.get("/projects", dependencies=[Depends(require_roles('admin'))])
async def list_projects(db: AsyncSession = Depends(get_db)):
    items = (await db.execute(select(Project))).scalars().all()
    return [{"id":x.id,"name":x.name} for x in items]

@router.get("/projects/{project_id}/keys", dependencies=[Depends(require_roles('admin'))])
async def list_keys(project_id: int, db: AsyncSession = Depends(get_db)):
    items = (await db.execute(select(ApiKey).where(ApiKey.project_id==project_id))).scalars().all()
    return [{"id":x.id,"key":x.key,"active":x.active} for x in items]
