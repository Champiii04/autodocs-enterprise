from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from html2docx import html2docx
from io import BytesIO
from ..storage import put_bytes
router = APIRouter()
@router.post("/save-html-to-docx")
async def save_html_to_docx(payload: dict):
    html = payload.get("html","")
    if not html: raise HTTPException(400, "html is required")
    buf = BytesIO(); html2docx(html, buf); data = buf.getvalue()
    key = "edited/edited.docx"
    put_bytes(key, data, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    return JSONResponse({"key": key})
