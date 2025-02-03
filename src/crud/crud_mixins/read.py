from typing import Generic, Optional, Sequence, Any
from uuid import UUID

from sqlalchemy import Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from constants.crud_types import ModelType


class ReadAsync(Generic[ModelType]):
    async def get(self, db: AsyncSession, obj_id: int) -> Optional[ModelType]:
        return await db.get(self.model, obj_id)

    async def get_all(
        self,
        db: AsyncSession,
        limit: int = 100,
        skip: int = 0,
    ) -> Sequence[Row[Any] | RowMapping | Any]:
        statement = select(self.model).offset(skip).limit(limit)
        result = await db.execute(statement)

        return result.scalars().all()

    async def get_by_uid(
        self, db: AsyncSession, *, uid: UUID
    ) -> Optional[ModelType]:
        statement = select(self.model).where(self.model.uid == uid)
        result = await db.execute(statement)
        return result.scalars().first()
