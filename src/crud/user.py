from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.async_crud import BaseAsyncCRUD
from models.user import User
from schemas.user import UserCreateDB, UserUpdateDB


class CRUDUser(BaseAsyncCRUD[User, UserCreateDB, UserUpdateDB]):
    async def check_for_user(self, db: AsyncSession, slug: str) -> bool:
        stmt = select(self.model).where(
            func.lower(self.model.username) == func.lower(slug)
        )
        result = await db.execute(stmt)
        return bool(result.fetchone()) is False

    async def get_by_email(
        self, db: AsyncSession, *, email: str
    ) -> Optional[User]:
        statement = select(self.model).where(self.model.email == email)
        result = await db.execute(statement)
        return result.scalars().first()

    async def get_by_username(
        self, db: AsyncSession, *, username: str
    ) -> Optional[User]:
        statement = select(self.model).where(self.model.username == username)
        result = await db.execute(statement)
        return result.scalars().first()

    async def get_admin(self, db: AsyncSession) -> bool:
        stmt = select(self.model).where(self.model.is_admin)
        result = await db.execute(stmt)
        return bool(result.fetchone())


crud_user = CRUDUser(User)
