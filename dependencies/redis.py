import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from fastapi import FastAPI
from redis import asyncio as aioredis

from custom_libs.fastapi_cache import FastAPICache
from custom_libs.fastapi_cache.backends.redis import RedisBackend


load_dotenv('.env')


@asynccontextmanager
async def redis_lifespan(app: FastAPI):
    redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379")
    try:
        redis = aioredis.from_url(
            redis_url, encoding="utf8", decode_responses=True
        )
        FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
        yield
    finally:
        await redis.close()
