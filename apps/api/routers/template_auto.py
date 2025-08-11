from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import SessionLocal
from ..models import Template, FormDefinition
from ..storage import put_bytes
from ..utils.doc_tools import ensure_docx, extract_placeholders
router = APIRouter()
async def get_db():
    async with SessionLocal() as s: yield s
@router.post("/autoform")
async def upload_template_autoform(key: str, name: str, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    if not (file.filename.endswith(".docx") or file.filename.endswith(".doc")): raise HTTPException(400, "Only .docx or .doc")
    raw = await file.read()
    try:
        docx_bytes = ensure_docx(raw, file.filename)
    except Exception as e:
        raise HTTPException(400, f"Cannot convert file: {e}")
    storage_key = f"templates/{key}.docx"
    put_bytes(storage_key, docx_bytes, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    t = Template(key=key, name=name, storage_key=storage_key); db.add(t); await db.commit(); await db.refresh(t)
    vars_ = extract_placeholders(docx_bytes)
    fields = [{"name":v,"label":v.replace('_',' ').title(),"type":"text","required":True,"options":[]} for v in vars_] or [{"name":"NOMBRE","label":"Nombre","type":"text","required":True,"options":[]}]
    f = FormDefinition(template_id=t.id, name=f"Formulario {name}", schema_json={"fields": fields}); db.add(f); await db.commit(); await db.refresh(f)
    return {"template": {"id": t.id, "key": t.key}, "form": {"id": f.id, "fields": len(fields), "schema": f.schema_json}}
