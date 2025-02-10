from typing import List
from uuid import UUID

from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.database import get_async_db
from api.dependencies.auth import get_current_user, get_admin
from models import User
from schemas.user import (
    UserResponse,
    UserCreate,
    UserUpdateFullDB,
    UserUpdateDB,
)
from services import user
from crud.user import crud_user

router = APIRouter()


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    create_data: UserCreate,
    db: AsyncSession = Depends(get_async_db),
):
    found_user = await crud_user.get_by_email(db, email=create_data.email)
    if found_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A user with this {create_data.email}, "
            f"already exists.",
        )
    return await user.create_user(db=db, create_data=create_data)


@router.get(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def get_account_for_user(
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.get(
    "/all/",
    response_model=List[UserResponse],
)
async def get_all_users(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
    limit: int = 100,
    skip: int = 0,
):
    return await crud_user.get_all(
        db=db,
        limit=limit,
        skip=skip,
    )


@router.get("/{user_uid}/", response_model=UserResponse)
async def get_user_by_uid(
    user_uid: UUID,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    if found_user := await crud_user.get_by_uid(db=db, uid=user_uid):
        return found_user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {user_uid} not found.",
    )


@router.patch(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def update_for_user(
    update_data: UserUpdateDB,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    if found_user := await crud_user.get_by_uid(db=db, uid=current_user.uid):
        return await user.update_user(
            db=db, found_user=found_user, update_data=update_data
        )


@router.patch(
    "/{user_uid}/",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def update_for_admin(
    user_uid: UUID,
    update_data: UserUpdateFullDB,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_admin),
):
    if found_user := await crud_user.get_by_uid(db=db, uid=current_user.uid):
        return await user.update_user(
            db=db,
            found_user=found_user,
            update_data=update_data,
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {user_uid} not found.",
    )


@router.delete("/{user_uid}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_uid: UUID,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    found_user = await crud_user.get_by_uid(db=db, uid=user_uid)
    if found_user and (
        found_user.uid == current_user.uid or current_user.is_admin is True
    ):
        found_user.is_deleted = True

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {user_uid} not found or you"
        f" don't have permission to delete this user.",
    )
