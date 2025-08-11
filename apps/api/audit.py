from .models import AuditLog
from .db import SessionLocal
from sqlalchemy.ext.asyncio import AsyncSession

async def log(actor_email: str, action: str, entity: str, entity_id: str, details: dict | None = None):
    async with SessionLocal() as s:  # type: AsyncSession
        s.add(AuditLog(actor_email=actor_email, action=action, entity=entity, entity_id=str(entity_id), details=details or {}))
        await s.commit()
