import asyncio, json, hashlib
from redis.asyncio import from_url as redis_from_url
from .settings import settings

redis = redis_from_url(settings.redis_url, decode_responses=False)

def make_key(template_key: str, tpl_bytes: bytes, data: dict) -> str:
    h = hashlib.sha256(tpl_bytes + json.dumps(data, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()
    return f"preview:{template_key}:{h}"

async def get_bytes(key: str) -> bytes | None:
    v = await redis.get(key)
    return v if v is None else bytes(v)

async def set_bytes(key: str, value: bytes, ttl: int = 300):
    await redis.set(key, value, ex=ttl)
