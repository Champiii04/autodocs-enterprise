from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import SessionLocal
from ..models import Template
from ..storage import put_bytes
from ..utils.doc_tools import ensure_docx
router = APIRouter()
MAX_MB = 20
import re
SAFE_KEY = re.compile(r"^[a-z0-9_\-]{3,64}$")
async def get_db():
    async with SessionLocal() as s: yield s
@router.post("")
async def create_template(key: str, name: str, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    if not SAFE_KEY.match(key): raise HTTPException(400, "template key inválida")
    if not (file.filename.endswith(".docx") or file.filename.endswith(".doc")): raise HTTPException(400, "Only .docx or .doc")
    if hasattr(file, 'size') and file.size and file.size > MAX_MB*1024*1024:
        raise HTTPException(413, "Archivo demasiado grande")
    raw = await file.read()
    try:
        docx = ensure_docx(raw, file.filename); storage_key = f"templates/{key}.docx"
        put_bytes(storage_key, docx, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    except Exception:
        storage_key = f"templates/{key}.doc"; put_bytes(storage_key, raw, "application/octet-stream")
    t = Template(key=key, name=name, storage_key=storage_key); db.add(t); await db.commit(); await db.refresh(t)
    return {"id": t.id, "key": t.key, "name": t.name, "storage_key": t.storage_key}
