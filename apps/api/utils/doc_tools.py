import os, re, tempfile, subprocess, zipfile, hashlib
from io import BytesIO

def ensure_docx(file_bytes: bytes, filename: str) -> bytes:
    if filename.lower().endswith(".docx"): return file_bytes
    with tempfile.TemporaryDirectory() as tmp:
        in_path = os.path.join(tmp, "in.doc"); out_path = os.path.join(tmp, "in.docx")
        with open(in_path, "wb") as f: f.write(file_bytes)
        subprocess.run(["soffice", "--headless", "--convert-to", "docx", "--outdir", tmp, in_path], check=True)
        with open(out_path, "rb") as f: return f.read()

def extract_placeholders(docx_bytes: bytes) -> list[str]:
    vars_set = set()
    with zipfile.ZipFile(BytesIO(docx_bytes)) as z: xml = z.read("word/document.xml").decode("utf-8", "ignore")
    for m in re.findall(r"\{\{\s*([^}\s][^}]*)\s*\}\}", xml): vars_set.add(m.strip())
    return sorted(vars_set)

def expand_equals_lines(docx_bytes: bytes, width: int = 110, marker: str = "=") -> bytes:
    # Reescribe document.xml expandiendo secuencias de '=' de longitud >=3 al ancho fijo
    with zipfile.ZipFile(BytesIO(docx_bytes)) as zin:
        xml = zin.read("word/document.xml").decode("utf-8", "ignore")
        def repl(m):
            seq = m.group(0)
            return marker * width
        new_xml = re.sub(rf"{re.escape(marker)}{{3,}}", repl, xml)
        # rebuild docx
        out = BytesIO()
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename == "word/document.xml":
                    zout.writestr(item, new_xml.encode("utf-8"))
                else:
                    zout.writestr(item, zin.read(item.filename))
        return out.getvalue()

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
