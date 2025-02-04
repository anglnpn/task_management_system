from typing import Any, Sequence

from sqlalchemy import Row, RowMapping, select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.async_crud import BaseAsyncCRUD
from models import Job
from schemas.job import JobCreateDB, JobUpdateDB


class CRUDJob(BaseAsyncCRUD[Job, JobCreateDB, JobUpdateDB]):
    async def get_by_author_id(
        self,
        db: AsyncSession,
        author_id: int,
    ) -> Sequence[Row[Any] | RowMapping | Any]:
        statement = select(self.model).where(self.model.author_id == author_id)
        result = await db.execute(statement)

        return result.scalars().all()

    async def get_by_performer_id(
        self,
        db: AsyncSession,
        performer_id: int,
    ) -> Sequence[Row[Any] | RowMapping | Any]:
        statement = select(self.model).where(
            self.model.performer_id == performer_id
        )
        result = await db.execute(statement)

        return result.scalars().all()


crud_job = CRUDJob(Job)
