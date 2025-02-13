import uuid
import pytest_asyncio

from datetime import datetime, UTC, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from crud.job import crud_job
from models import User, Job
from schemas.job import JobCreateDB


@pytest_asyncio.fixture
async def job_fixture(
    async_session: AsyncSession, user_fixture: User, user_fixture_2: User
) -> Job:
    schema = JobCreateDB(
        title="Test job",
        description="Test description",
        deadline=datetime.now(tz=UTC) + timedelta(days=5),
        author_id=user_fixture.id,
        performer_id=user_fixture_2.id,
        uid=uuid.uuid4(),
    )
    new_job = await crud_job.create(db=async_session, create_schema=schema)
    return new_job


@pytest_asyncio.fixture
async def job_fixture_2(
    async_session: AsyncSession, user_fixture: User, user_fixture_2: User
) -> Job:
    schema = JobCreateDB(
        title="Test job 2",
        description="Test description",
        deadline=datetime.now(tz=UTC) + timedelta(days=10),
        author_id=user_fixture.id,
        performer_id=user_fixture_2.id,
        uid=uuid.uuid4(),
    )
    new_job = await crud_job.create(db=async_session, create_schema=schema)
    return new_job
