from uuid import UUID

from pydantic import BaseModel


class UserLogin(BaseModel):
    email: str
    password: str


class TokenAccessRefresh(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenPayload(BaseModel):
    uid: UUID


class AuthURLResponse(BaseModel):
    url: str
