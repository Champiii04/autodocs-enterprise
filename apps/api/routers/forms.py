from fastapi import APIRouter, HTTPException, Depends
from ..auth import require_roles
from ..audit import log
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..db import SessionLocal
from ..models import FormDefinition, Template
router = APIRouter()
async def get_db():
    async with SessionLocal() as s: yield s
@router.get("/{template_key}")
async def get_form_by_template_key(template_key: str, db: AsyncSession = Depends(get_db)):
    t = (await db.execute(select(Template).where(Template.key == template_key))).scalar_one_or_none()
    if not t: raise HTTPException(404, "Template not found")
    f = (await db.execute(select(FormDefinition).where(FormDefinition.template_id == t.id))).scalar_one_or_none()
    if not f: raise HTTPException(404, "Form not found for template")
    return {"id": f.id, "name": f.name, "schema": f.schema_json}
@router.put("/{form_id}")
async def update_form(form_id: int, payload: dict, db: AsyncSession = Depends(get_db), user: dict = Depends(require_roles('admin','notary','assistant'))):
    f = (await db.execute(select(FormDefinition).where(FormDefinition.id == form_id))).scalar_one_or_none()
    if not f: raise HTTPException(404, "Form not found")
    f.schema_json = payload.get("schema", f.schema_json); await db.commit(); await db.refresh(f)
    await log(user['sub'], 'update', 'FormDefinition', f.id, {'schema_size': len(str(f.schema_json))})
    return {"ok": True, "id": f.id}
