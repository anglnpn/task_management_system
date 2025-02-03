from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from schemas.password import PasswordBase


class UserBase(BaseModel):
    first_name: str
    second_name: str
    email: str

    class Config:
        from_attributes = True


class UserCreate(PasswordBase, UserBase):
    pass


class UserCreateDB(UserBase):
    uid: UUID
    username: str
    hashed_password: str


class UserUpdate(UserBase):
    first_name: Optional[str] = None
    second_name: Optional[str] = None
    username: Optional[str] = Field(None, max_length=25, min_length=5)


class UserUpdateFull(UserUpdate):
    is_admin: Optional[bool] = None
    is_deleted: Optional[bool] = None


class UserUpdateDB(UserUpdate):
    pass


class UserUpdateFullDB(UserUpdateFull):
    pass


class UserResponse(UserBase):
    uid: UUID
    username: Optional[str] = None
