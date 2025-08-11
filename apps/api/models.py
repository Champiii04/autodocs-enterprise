from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, ForeignKey, DateTime, JSON, func, Boolean, Text
class Base(DeclarativeBase): pass
class User(Base):
    __tablename__="users"
    id: Mapped[int]=mapped_column(primary_key=True)
    email: Mapped[str]=mapped_column(String(255), unique=True, index=True)
    role: Mapped[str]=mapped_column(String(32), default="client") # admin, notary, assistant, client
    password_hash: Mapped[str]=mapped_column(String(255), default="")
    active: Mapped[bool]=mapped_column(Boolean, default=True)
class Template(Base):
    __tablename__ = "templates"
    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    storage_key: Mapped[str] = mapped_column(String(1024))
    metadata_json: Mapped[dict] = mapped_column(JSON, default={})
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
class FormDefinition(Base):
    __tablename__ = "form_definitions"
    id: Mapped[int] = mapped_column(primary_key=True)
    template_id: Mapped[int] = mapped_column(ForeignKey("templates.id"))
    name: Mapped[str] = mapped_column(String(255))
    schema_json: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
class Job(Base):
    __tablename__ = "jobs"
    id: Mapped[int] = mapped_column(primary_key=True)
    template_id: Mapped[int] = mapped_column(ForeignKey("templates.id"))
    status: Mapped[str] = mapped_column(String(32), default="queued")
    input_json: Mapped[dict] = mapped_column(JSON)
    output_docx_key: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    output_pdf_key: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    output_odt_key: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    output_html_key: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    hash_sha256: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
class AuditLog(Base):
    __tablename__="audit_logs"
    id: Mapped[int]=mapped_column(primary_key=True)
    actor_email: Mapped[str]=mapped_column(String(255))
    action: Mapped[str]=mapped_column(String(64))
    entity: Mapped[str]=mapped_column(String(64))
    entity_id: Mapped[str]=mapped_column(String(64))
    details: Mapped[dict]=mapped_column(JSON, default={})
    created_at: Mapped[DateTime]=mapped_column(DateTime(timezone=True), server_default=func.now())

class Project(Base):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)

class ApiKey(Base):
    __tablename__ = "api_keys"
    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    key: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
