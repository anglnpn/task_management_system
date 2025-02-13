import sys
from typing import Callable, Generator

import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from databases.database import async_engine
from main import lifespan, create_app
from models import User
from models.base import Base
from security.token import access_security

from .fixtures import *  # noqa: F403

assert (sys.version_info.major, sys.version_info.minor) == (
    3,
    11,
), "Only Python 3.11 allowed"


@pytest_asyncio.fixture
async def async_session() -> AsyncSession:
    session = sessionmaker(
        async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with session() as s:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        yield s

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await async_engine.dispose()


@pytest_asyncio.fixture
async def http_client(
    async_session: AsyncSession,
) -> Generator[AsyncClient, None, None]:
    test_app = create_app()
    async with (
        lifespan(test_app),
        AsyncClient(app=test_app, base_url="http://0.0.0.0:8000") as ac,
    ):
        yield ac


@pytest_asyncio.fixture
async def get_auth_headers() -> Callable:
    async def _get_auth_headers(user: User) -> dict:
        subject = {"uid": str(user.uid)}
        access_token = access_security.create_access_token(subject=subject)
        headers = {"Authorization": f"Bearer {access_token}"}
        return headers

    return _get_auth_headers
