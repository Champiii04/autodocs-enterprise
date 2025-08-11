from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from io import BytesIO
from ..db import SessionLocal
from ..models import Template, FormDefinition
from sqlalchemy import select as sa_select
from ..validation import model_from_schema
from ..storage import get_bytes
from ..cache import make_key, get_bytes as cache_get, set_bytes as cache_set
from apps.worker.renderer.docx_engine import render_docx_from_bytes
router = APIRouter()
async def get_db():
    async with SessionLocal() as s: yield s
@router.post("/{template_key}")
async def preview(template_key: str, payload: dict, db: AsyncSession = Depends(get_db)):
    t = (await db.execute(select(Template).where(Template.key == template_key))).scalar_one_or_none()
    if not t: raise HTTPException(404, "Template not found")
    # validate input against schema
    f = (await db.execute(sa_select(FormDefinition).where(FormDefinition.template_id == t.id))).scalar_one_or_none()
    if f:
        Form = model_from_schema(f.schema_json)
        try:
            _ = Form(**payload.get('data', {}))
        except Exception as e:
            raise HTTPException(422, f"Datos inválidos: {e}")
    tpl = get_bytes(t.storage_key)
    data = payload.get('data', {})
    ckey = make_key(t.key, tpl, data)
    cached = await cache_get(ckey)
    if cached:
        return StreamingResponse(BytesIO(cached), media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f"attachment; filename={template_key}_preview.docx"})
    out = render_docx_from_bytes(tpl, data)
    await cache_set(ckey, out, ttl=300)
    return StreamingResponse(BytesIO(out), media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                             headers={"Content-Disposition": f"attachment; filename={template_key}_preview.docx"})
