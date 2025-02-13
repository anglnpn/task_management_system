from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, EmailStr

from schemas.password import PasswordBase


class UserBase(BaseModel):
    first_name: str = Field(min_length=2, max_length=30)
    second_name: str = Field(min_length=2, max_length=30)
    email: EmailStr = Field(min_length=2)

    class Config:
        from_attributes = True


class UserCreate(PasswordBase, UserBase):
    pass


class UserCreateDB(UserBase):
    uid: UUID
    username: str
    hashed_password: str


class AdminCreateDB(UserCreateDB):
    is_admin: bool = Field(default=True)


class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=2, max_length=30)
    second_name: Optional[str] = Field(None, min_length=2, max_length=30)
    username: Optional[str] = Field(None, max_length=25, min_length=5)
    email: Optional[EmailStr] = Field(None, min_length=2)


class UserUpdateFull(UserUpdate):
    is_admin: Optional[bool] = None
    is_deleted: Optional[bool] = None


class UserUpdateDB(UserUpdate):
    pass


class UserUpdateFullDB(UserUpdateFull):
    pass


class UserResponse(UserBase):
    id: int
    uid: UUID
    username: Optional[str] = None


class UserForAdminResponse(UserResponse):
    is_admin: bool
    is_deleted: bool
