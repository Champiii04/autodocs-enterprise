from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, desc, and_
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import SessionLocal
from ..models import Job
from ..storage import presign_get_url

router = APIRouter()
async def get_db():
    async with SessionLocal() as s: yield s

@router.get("/search")
async def search(status: str | None = None, start_id: int | None = None, end_id: int | None = None, limit: int = 200, db: AsyncSession = Depends(get_db)):
    conds = []
    if status: conds.append(Job.status == status)
    if start_id: conds.append(Job.id >= start_id)
    if end_id: conds.append(Job.id <= end_id)
    stmt = select(Job).order_by(desc(Job.id)).limit(limit)
    if conds: stmt = stmt.where(and_(*conds))
    res = (await db.execute(stmt)).scalars().all()
    out = []
    for j in res:
        out.append({
            "id": j.id,
            "status": j.status,
            "template_id": j.template_id,
            "created_at": str(j.created_at),
            "docx": presign_get_url(j.output_docx_key) if j.output_docx_key else None,
            "pdf":  presign_get_url(j.output_pdf_key) if j.output_pdf_key else None
        })
    return out

@router.get("/recent")
async def recent(limit: int = 100, db: AsyncSession = Depends(get_db)):
    res = (await db.execute(select(Job).order_by(desc(Job.id)).limit(limit))).scalars().all()
    return [{
        "id":j.id,"status":j.status,"template_id":j.template_id,"created_at":str(j.created_at),
        "docx": presign_get_url(j.output_docx_key) if j.output_docx_key else None,
        "pdf":  presign_get_url(j.output_pdf_key) if j.output_pdf_key else None
    } for j in res]
