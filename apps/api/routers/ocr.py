from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from ..auth import require_roles
import pytesseract
from PIL import Image
import io
router = APIRouter()
@router.post("/scan")
async def scan(file: UploadFile = File(...), user: dict = Depends(require_roles('admin','notary','assistant'))):
    if not file.filename.lower().endswith((".png",".jpg",".jpeg")):
        raise HTTPException(400, "Use PNG/JPG")
    img = Image.open(io.BytesIO(await file.read()))
    text = pytesseract.image_to_string(img, lang="spa")
    return {"text": text}
