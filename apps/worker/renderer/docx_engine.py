from io import BytesIO
from docxtpl import DocxTemplate
def pad_filter(val, width=60, ch='='):
    s = str(val or '')
    if len(s) >= width: return s
    return s + ch * (width - len(s))
def render_docx_from_bytes(template_bytes: bytes, context: dict) -> bytes:
    doc = DocxTemplate(BytesIO(template_bytes))
    doc.jinja_env.filters['pad'] = pad_filter
    doc.render(context)
    out = BytesIO(); doc.save(out); return out.getvalue()
