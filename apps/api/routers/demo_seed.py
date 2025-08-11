from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..db import SessionLocal
from ..models import Template, FormDefinition
from ..storage import put_bytes
from ..utils.doc_tools import ensure_docx, extract_placeholders
import os

router = APIRouter()
async def get_db():
    async with SessionLocal() as s: yield s

@router.post("/seed")
async def seed(db: AsyncSession = Depends(get_db)):
    # Load local asset (included in repo)
    path = "assets/sample/poder_amplio.doc"
    if not os.path.exists(path): raise HTTPException(500, "Sample DOC not found in assets")
    raw = open(path, "rb").read()
    docx_bytes = ensure_docx(raw, "poder_amplio.doc")
    key = "poder_amplio"
    storage_key = f"templates/{key}.docx"
    put_bytes(storage_key, docx_bytes, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    # Create template
    t = Template(key=key, name="Poder Amplio", storage_key=storage_key)
    db.add(t); await db.commit(); await db.refresh(t)
    # Extract vars and add a conditional 'ALCANCE' when PODER_TIPO == 'ESPECIAL'
    vars_ = extract_placeholders(docx_bytes)
    fields = [{"name":v,"label":v.replace('_',' ').title(),"type":"text","required":True,"options":[]} for v in vars_]
    # Example conditional
    fields.append({"name":"ALCANCE","label":"Alcance","type":"textarea","required":False,"options":[],"show_if":{"field":"PODER_TIPO","equals":"ESPECIAL"}})
    f = FormDefinition(template_id=t.id, name="Formulario Poder Amplio", schema_json={"fields": fields})
    db.add(f); await db.commit(); await db.refresh(f)
    return {"template_key": key, "form_id": f.id, "fields": len(fields)}
