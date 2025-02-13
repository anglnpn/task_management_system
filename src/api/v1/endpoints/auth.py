from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse, Response

from api.dependencies.database import get_async_db
from crud.user import crud_user
from schemas.token import TokenAccessRefresh, UserLogin
from security.password import verify_password
from security.token import (
    ACCESS_TOKEN_COOKIE_KEY,
    REFRESH_TOKEN_COOKIE_KEY,
    access_security,
    refresh_security,
)
from utilities.tokens import create_tokens, set_tokens_to_cookie

router = APIRouter()


@router.post("/login/", response_model=TokenAccessRefresh)
async def login(
    user_login: UserLogin, db: AsyncSession = Depends(get_async_db)
):
    found_user = await crud_user.get_by_email(db, email=user_login.email)
    if not found_user or found_user.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_login.email} not found.",
        )

    password_verified = await verify_password(
        plain_password=user_login.password,
        hashed_password=found_user.hashed_password,
    )
    if not password_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User password is wrong",
        )

    tokens = await create_tokens(subject={"uid": str(found_user.uid)})
    response = JSONResponse(content=tokens.model_dump())
    return await set_tokens_to_cookie(response=response, tokens=tokens)


@router.post("/refresh/", response_model=TokenAccessRefresh)
async def refresh(
    credentials: JwtAuthorizationCredentials = Security(refresh_security),
):
    return await create_tokens(credentials.subject)


@router.delete("/logout/", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    response = Response()
    response.delete_cookie(ACCESS_TOKEN_COOKIE_KEY)
    response.delete_cookie(REFRESH_TOKEN_COOKIE_KEY)
    return response
