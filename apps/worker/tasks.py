from .celery_app import celery
from .renderer.docx_engine import render_docx_from_bytes
from .renderer.pdf_engine import docx_to_pdf, docx_to_odt, docx_to_html
import boto3, os, asyncio
from apps.api.utils.doc_tools import expand_equals_lines, sha256
S3_ENDPOINT=os.getenv("S3_ENDPOINT"); S3_ACCESS_KEY=os.getenv("S3_ACCESS_KEY"); S3_SECRET_KEY=os.getenv("S3_SECRET_KEY")
S3_BUCKET=os.getenv("S3_BUCKET"); S3_REGION=os.getenv("S3_REGION","us-east-1")
s3 = boto3.client("s3", **({"endpoint_url": S3_ENDPOINT} if S3_ENDPOINT else {}),
    aws_access_key_id=S3_ACCESS_KEY, aws_secret_access_key=S3_SECRET_KEY, region_name=S3_REGION)
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from apps.api.models import Job, Template
from apps.api.settings import settings
from sqlalchemy import select
engine = create_async_engine(settings.database_url); SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

@celery.task(name="tasks.render_doc")
def render_doc(job_id: int, template_key: str, template_storage_key: str, data: dict, options: dict):
    tpl = s3.get_object(Bucket=S3_BUCKET, Key=template_storage_key)["Body"].read()
    # Render DOCX
    docx_bytes = render_docx_from_bytes(tpl, data)
    # Expand '====' filler lines to uniform width
    docx_bytes = expand_equals_lines(docx_bytes, width=110, marker='=')
    # Convert formats
    want = options.get("format","both")
    pdf_bytes = docx_to_pdf(docx_bytes) if want in ("pdf","both") else None
    odt_bytes = docx_to_odt(docx_bytes) if want in ("odt","both") else None
    html_bytes = docx_to_html(docx_bytes) if want in ("html","both") else None
    # Upload
    base = f"outputs/{job_id or 'batch'}/{template_key}"
    docx_key = f"{base}.docx"; s3.put_object(Bucket=S3_BUCKET, Key=docx_key, Body=docx_bytes, ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    pdf_key = odt_key = html_key = None
    if pdf_bytes: pdf_key = f"{base}.pdf";  s3.put_object(Bucket=S3_BUCKET, Key=pdf_key,  Body=pdf_bytes, ContentType="application/pdf")
    if odt_bytes: odt_key = f"{base}.odt";  s3.put_object(Bucket=S3_BUCKET, Key=odt_key,  Body=odt_bytes, ContentType="application/vnd.oasis.opendocument.text")
    if html_bytes: html_key = f"{base}.html"; s3.put_object(Bucket=S3_BUCKET, Key=html_key, Body=html_bytes, ContentType="text/html; charset=utf-8")
    # Persist job if not batch
    if job_id:
        async def update_job():
            async with SessionLocal() as s:
                j = (await s.execute(select(Job).where(Job.id==job_id))).scalar_one()
                j.status="done"; j.hash_sha256=sha256(docx_bytes); j.output_docx_key=docx_key
                j.output_pdf_key=pdf_key; j.output_odt_key=odt_key; j.output_html_key=html_key
                await s.commit()
        asyncio.run(update_job())
    return True
