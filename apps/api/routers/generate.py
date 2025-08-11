from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from ..auth import require_roles
from ..audit import log
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import SessionLocal
from ..models import Template, Job, FormDefinition
from ..validation import model_from_schema
from sqlalchemy import select as sa_select
from ..schemas import GenerateRequest, JobOut
from ..settings import settings
from ..storage import presign_get_url
from celery import Celery
import csv, io
router = APIRouter()
celery = Celery(broker=settings.celery_broker_url, backend=settings.celery_result_backend)
async def get_db():
    async with SessionLocal() as s: yield s
@router.post("/{template_key}", response_model=JobOut)
async def generate(template_key: str, payload: GenerateRequest, db: AsyncSession = Depends(get_db), user: dict = Depends(require_roles('admin','notary','assistant','client'))):
    t = (await db.execute(select(Template).where(Template.key == template_key))).scalar_one_or_none()
    f = (await db.execute(sa_select(FormDefinition).where(FormDefinition.template_id == (t.id if t else -1)))).scalar_one_or_none()
    if f:
        Form = model_from_schema(f.schema_json)
        try:
            _ = Form(**payload.data)
        except Exception as e:
            raise HTTPException(422, f"Datos inválidos: {e}")
    if not t: raise HTTPException(404, "Template not found")
    job = Job(template_id=t.id, status="queued", input_json=payload.data); db.add(job); await db.commit(); await db.refresh(job)
    celery.send_task("tasks.render_doc", args=[job.id, t.key, t.storage_key, payload.data, payload.options], queue="default")
    await log(user['sub'], 'generate', 'Job', job.id, {'template_key': t.key})
    return JobOut(id=job.id, status=job.status)
@router.post("/{template_key}/batch")
async def generate_batch(template_key: str, file: UploadFile = File(...), db: AsyncSession = Depends(get_db), user: dict = Depends(require_roles('admin','notary'))):
    t = (await db.execute(select(Template).where(Template.key == template_key))).scalar_one_or_none()
    f = (await db.execute(sa_select(FormDefinition).where(FormDefinition.template_id == (t.id if t else -1)))).scalar_one_or_none()
    if f:
        Form = model_from_schema(f.schema_json)
        try:
            _ = Form(**payload.data)
        except Exception as e:
            raise HTTPException(422, f"Datos inválidos: {e}")
    if not t: raise HTTPException(404, "Template not found")
    raw = await file.read()
    text = raw.decode("utf-8", "ignore")
    reader = csv.DictReader(io.StringIO(text))
    count = 0
    for row in reader:
        celery.send_task("tasks.render_doc", args=[0, t.key, t.storage_key, row, {"format":"pdf"}], queue="batch")
        count += 1
    await log(user['sub'], 'generate_batch', 'Template', t.id, {'rows': count})
    return {"queued": count}
@router.get("/signed-url/{key}")
async def get_signed_url(key: str):
    return {"url": presign_get_url(key)}
