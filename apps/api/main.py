from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter
from prometheus_fastapi_instrumentator import Instrumentator
import bcrypt
from sqlalchemy import select
from slowapi.util import get_remote_address
from .settings import settings
from .models import Base
from .db import engine
from sqlalchemy import text
from .routers import templates, template_auto, forms, generate, jobs, presets, ocr
from apps.ui.routes import router as ui_router
app = FastAPI(title="Tramita Ya Autodocs Enterprise")
limiter = Limiter(key_func=get_remote_address, default_limits=[settings.rate_limit])
app.state.limiter = limiter

@app.on_event("startup")
async def startup():
    from .models import User
    from sqlalchemy import select as sa_select
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Optional admin seed (only if provided)
    from .settings import settings
    if settings.admin_email and settings.admin_password:
        from .db import SessionLocal
        async with SessionLocal() as s:
            u = (await s.execute(sa_select(User).where(User.email==settings.admin_email))).scalar_one_or_none()
            if not u:
                import bcrypt
                ph = bcrypt.hashpw(settings.admin_password.encode(), bcrypt.gensalt()).decode()
                u = User(email=settings.admin_email, role=(settings.admin_role or 'admin'), active=True, password_hash=ph)
                s.add(u); await s.commit()
@app.get("/healthz")
async def healthz():
    return {"ok": True}
  
Instrumentator().instrument(app).expose(app, endpoint="/metrics")
app.include_router(templates.router, prefix="/v1/templates", tags=["templates"])
app.include_router(forms.router,    prefix="/v1/forms",    tags=["forms"])
app.include_router(template_auto.router, prefix="/v1/templates", tags=["templates"])
app.include_router(generate.router, prefix="/v1/generate", tags=["generate"])
app.include_router(jobs.router,     prefix="/v1/jobs",     tags=["jobs"])
app.include_router(presets.router,  prefix="/v1/presets",  tags=["presets"])
app.include_router(ocr.router,      prefix="/v1/ocr",      tags=["ocr"])
app.include_router(ui_router, prefix="/ui", tags=["ui"])
app.mount("/static", StaticFiles(directory="apps/ui/static"), name="static")
