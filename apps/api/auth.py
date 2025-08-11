import time, jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .settings import settings

bearer = HTTPBearer(auto_error=False)

def create_token(email: str, role: str, ttl_sec: int = 86400) -> str:
    now = int(time.time())
    payload = {"sub": email, "role": role, "iat": now, "exp": now + ttl_sec}
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
    except jwt.PyJWTError:
        raise HTTPException(401, "Token inválido")

def get_current_user(creds: HTTPAuthorizationCredentials = Depends(bearer)) -> dict:
    if not creds: raise HTTPException(401, "Autorización requerida")
    return decode_token(creds.credentials)

def require_roles(*roles):
    def _dep(user: dict = Depends(get_current_user)):
        if user.get("role") not in roles:
            raise HTTPException(403, "No autorizado")
        return user
    return _dep
