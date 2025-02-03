from typing import Generic

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import undefer

from constants.crud_types import CreateSchemaType, ModelType


class CreateAsync(Generic[CreateSchemaType, ModelType]):
    async def create(
        self,
        db: AsyncSession,
        *,
        create_schema: CreateSchemaType,
        commit: bool = True,
    ) -> ModelType:
        data = create_schema.model_dump(exclude_unset=True)
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await db.execute(stmt)
        obj = res.scalars().first()
        if commit:
            await db.commit()
            await db.refresh(obj)
        return obj

    async def create_new_i18n(
        self,
        db: AsyncSession,
        *,
        create_schema: CreateSchemaType,
        commit: bool = True,
    ) -> ModelType:
        data = create_schema.model_dump(exclude_unset=True)
        stmt = (
            insert(self.model)
            .values(**data)
            .options(
                undefer(
                    self.model.name_ru,
                )
            )
            .returning(self.model)
        )
        res = await db.execute(stmt)
        obj = res.scalars().first()
        if commit:
            await db.commit()
            await db.refresh(obj)
        return obj
