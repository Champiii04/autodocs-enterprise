from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import SessionLocal
from ..models import Job
from ..schemas import JobOut
from ..storage import presign_get_url
router = APIRouter()
async def get_db():
    async with SessionLocal() as s: yield s
@router.get("/{job_id}", response_model=JobOut)
async def get_job(job_id: int, db: AsyncSession = Depends(get_db)):
    j = (await db.execute(select(Job).where(Job.id == job_id))).scalar_one_or_none()
    if not j: raise HTTPException(404, "Job not found")
    return JobOut(
        id=j.id, status=j.status,
        output_docx_url=presign_get_url(j.output_docx_key) if j.output_docx_key else None,
        output_pdf_url=presign_get_url(j.output_pdf_key) if j.output_pdf_key else None,
        output_odt_url=presign_get_url(j.output_odt_key) if j.output_odt_key else None,
        output_html_url=presign_get_url(j.output_html_key) if j.output_html_key else None,
    )
