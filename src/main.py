from contextlib import asynccontextmanager
from typing import AsyncContextManager

from redis import asyncio as aioredis
import uvicorn

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.v1.router import router as v1_router
from configs.config import app_settings, redis_settings
from configs.loggers import logger


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncContextManager[None]:
    logger.info("Startup redis connection")
    redis_from_url = await aioredis.from_url(
        f"redis://{redis_settings.REDIS_HOST}:{redis_settings.REDIS_PORT}",
        encoding="utf8",
        decode_responses=True,
    )
    app.state.redis = redis_from_url
    yield
    logger.info("Shutdown redis connection")
    await redis_from_url.close()


def create_app() -> FastAPI:
    app = FastAPI(
        title=app_settings.SERVICE_NAME,
        openapi_url="/openapi.json",
        docs_url="/docs",
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(
        v1_router, prefix=f"/api/{app_settings.SERVICE_VERSION}"
    )
    return app


app = create_app()

if __name__ == "__main__":
    host = "0.0.0.0"  # noqa: S104
    uvicorn.run(
        "main:app",
        host=host,
        port=app_settings.SERVICE_PORT,
        reload=True,
        forwarded_allow_ips="*",
    )
