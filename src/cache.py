from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from configs.config import redis_settings


async def start_cache() -> None:
    redis = aioredis.from_url(
        f"redis://{redis_settings.REDIS_HOST}",
        encoding="utf8",
        decode_responses=False,
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
