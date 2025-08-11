import boto3
from .settings import settings
_session = boto3.session.Session()
_s3 = _session.client("s3",
    **({"endpoint_url": settings.s3_endpoint} if settings.s3_endpoint else {}),
    aws_access_key_id=settings.s3_access_key,
    aws_secret_access_key=settings.s3_secret_key,
    region_name=settings.s3_region,
)
def put_bytes(key: str, data: bytes, content_type: str) -> str:
    _s3.put_object(Bucket=settings.s3_bucket, Key=key, Body=data, ContentType=content_type,
                   ServerSideEncryption="AES256")
    return key
def get_bytes(key: str) -> bytes:
    r = _s3.get_object(Bucket=settings.s3_bucket, Key=key); return r["Body"].read()
def presign_get_url(key: str, expires: int = 3600) -> str:
    return _s3.generate_presigned_url("get_object", Params={"Bucket": settings.s3_bucket, "Key": key}, ExpiresIn=expires)
