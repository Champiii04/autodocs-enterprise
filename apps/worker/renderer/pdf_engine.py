import subprocess, tempfile, os
def convert_with_soffice(in_bytes: bytes, in_ext: str, out_ext: str) -> bytes:
    with tempfile.TemporaryDirectory() as tmp:
        in_path = os.path.join(tmp, f"in.{in_ext}"); out_path = os.path.join(tmp, f"in.{out_ext}")
        with open(in_path, "wb") as f: f.write(in_bytes)
        subprocess.run(["soffice","--headless","--convert-to",out_ext,"--outdir",tmp,in_path], check=True)
        with open(out_path, "rb") as f: return f.read()
def docx_to_pdf(docx_bytes: bytes) -> bytes: return convert_with_soffice(docx_bytes, "docx", "pdf")
def docx_to_odt(docx_bytes: bytes) -> bytes: return convert_with_soffice(docx_bytes, "docx", "odt")
def docx_to_html(docx_bytes: bytes) -> bytes: return convert_with_soffice(docx_bytes, "docx", "html")
