from contextlib import asynccontextmanager
from typing import AsyncContextManager

from redis import asyncio as aioredis
import uvicorn

from fastapi import FastAPI
from sqladmin import Admin
from starlette.middleware.cors import CORSMiddleware

from api.admin.admin import load_admin_site
from api.admin.views.auth import AdminAuth
from api.v1.router import router as v1_router
from cache import start_cache
from crud.user import crud_user
from configs.config import app_settings, redis_settings
from configs.loggers import logger
from databases.database import async_engine, async_session
from services.user import create_admin


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncContextManager[None]:
    logger.info("Startup redis connection")
    redis_from_url = await aioredis.from_url(
        f"redis://{redis_settings.REDIS_HOST}:{redis_settings.REDIS_PORT}",
        encoding="utf8",
        decode_responses=True,
    )
    app.state.redis = redis_from_url

    await start_cache()

    async with async_session() as db:
        admin_exists = await crud_user.get_admin(db)
        if not admin_exists:
            logger.info("Admin not found, creating a new one...")
            await create_admin(db)
        else:
            logger.info("Admin already exists, skipping creation.")

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
    app.include_router(v1_router, prefix="/api")
    return app


def connect_admin(app: FastAPI) -> None:
    authentication_backend = AdminAuth(
        secret_key=app_settings.SECRET_KEY_ADMIN
    )
    admin = Admin(
        app,
        async_engine,
        title="task management",
        base_url="/admin",
        authentication_backend=authentication_backend,
    )
    load_admin_site(admin)


app = create_app()
connect_admin(app)

if __name__ == "__main__":
    host = "0.0.0.0"  # noqa: S104
    uvicorn.run(
        "main:app",
        host=host,
        port=app_settings.SERVICE_PORT,
        reload=True,
        forwarded_allow_ips="*",
    )
