from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..db import SessionLocal
from ..models import User
from ..auth import create_token
import bcrypt

router = APIRouter()
async def get_db():
    async with SessionLocal() as s: yield s

class Login(BaseModel):
    email: EmailStr
    password: str

@router.post("/login")
async def login(payload: Login, db: AsyncSession = Depends(get_db)):
    u = (await db.execute(select(User).where(User.email==payload.email, User.active==True))).scalar_one_or_none()
    if not u or not u.password_hash or not bcrypt.checkpw(payload.password.encode(), u.password_hash.encode()):
        raise HTTPException(401, "Credenciales inválidas")
    return {"access_token": create_token(u.email, u.role), "role": u.role}
