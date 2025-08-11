from pydantic_settings import BaseSettings
from pydantic import field_validator
class Settings(BaseSettings):
    admin_email: str | None = None
    admin_password: str | None = None
    admin_role: str | None = None
    database_url: str
    redis_url: str
    celery_broker_url: str
    celery_result_backend: str
    s3_endpoint: str | None = None
    s3_access_key: str
    s3_secret_key: str
    s3_bucket: str
    s3_region: str = "us-east-1"
    jwt_secret: str = "change-me"
    rate_limit: str = "200/minute"
    pii_enc_key: str = "change-me-32bytes"
    model_config = {"env_file": ".env","env_file_encoding":"utf-8","case_sensitive":False}
settings = Settings()

    @field_validator("jwt_secret","pii_enc_key")
    @classmethod
    def _not_default(cls, v, info):
        if not v or "change-me" in v.lower():
            raise ValueError(f"{info.field_name} debe venir de entorno y no usar defaults")
        return v
    