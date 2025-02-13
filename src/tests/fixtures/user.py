import uuid

import pytest_asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from schemas.user import UserCreateDB
from security.password import hash_password
from crud.user import crud_user


@pytest_asyncio.fixture
async def user_fixture(async_session: AsyncSession) -> User:
    schema = UserCreateDB(
        uid=uuid.uuid4(),
        username="test_user",
        hashed_password=await hash_password("password"),
        first_name="Test",
        second_name="User",
        email="test@gmail.com",
    )
    new_user = await crud_user.create(db=async_session, create_schema=schema)
    return new_user


@pytest_asyncio.fixture
async def user_fixture_2(async_session: AsyncSession) -> User:
    schema = UserCreateDB(
        uid=uuid.uuid4(),
        username="test_user_2",
        hashed_password=await hash_password("password"),
        first_name="Test2",
        second_name="User2",
        email="test2@gmail.com",
    )
    new_user = await crud_user.create(db=async_session, create_schema=schema)
    return new_user


@pytest_asyncio.fixture
async def user_fixture_3(async_session: AsyncSession) -> User:
    schema = UserCreateDB(
        uid=uuid.uuid4(),
        username="admin2",
        hashed_password=await hash_password("password"),
        first_name="admin",
        second_name="admin",
        email="admin2@gmail.com",
    )
    new_user = await crud_user.create(db=async_session, create_schema=schema)
    new_user.is_admin = True

    async_session.add(new_user)
    await async_session.commit()
    await async_session.refresh(new_user)

    return new_user
