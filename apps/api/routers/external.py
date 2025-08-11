from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import SessionLocal
from ..models import Template, Job
from ..schemas import GenerateRequest, JobOut
from ..settings import settings
from celery import Celery
from ..api_keys import require_api_key

router = APIRouter()
celery = Celery(broker=settings.celery_broker_url, backend=settings.celery_result_backend)
async def get_db():
    async with SessionLocal() as s: yield s

@router.post("/generate/{template_key}", response_model=JobOut)
async def generate_external(template_key: str, payload: GenerateRequest, db: AsyncSession = Depends(get_db), project = Depends(require_api_key)):
    t = (await db.execute(select(Template).where(Template.key == template_key))).scalar_one_or_none()
    if not t: raise HTTPException(404, "Template not found")
    job = Job(template_id=t.id, status="queued", input_json=payload.data); db.add(job); await db.commit(); await db.refresh(job)
    celery.send_task("tasks.render_doc", args=[job.id, t.key, t.storage_key, payload.data, payload.options], queue="default")
    return JobOut(id=job.id, status=job.status)
