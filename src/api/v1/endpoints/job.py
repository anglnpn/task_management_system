import uuid
from typing import List
from uuid import UUID

from fastapi import APIRouter, status, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from configs.loggers import logger
from api.dependencies.database import get_async_db
from api.dependencies.auth import get_current_user
from crud.job import crud_job
from models.user import User
from schemas.job import (
    JobResponse,
    JobCreate,
    JobUpdate,
    JobUpdateForPerformer,
    JobCreateDB,
)

router = APIRouter()


@router.get(
    "/author/",
    response_model=List[JobResponse],
    status_code=status.HTTP_200_OK,
)
@cache(expire=60)
async def get_author_jobs(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    return await crud_job.get_by_author_id(db=db, author_id=current_user.id)


@router.get(
    "/performer/",
    response_model=List[JobResponse],
    status_code=status.HTTP_200_OK,
)
@cache(expire=60)
async def get_performer_jobs(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    return await crud_job.get_by_performer_id(
        db=db, performer_id=current_user.id
    )


@router.get("/all/", response_model=List[JobResponse])
@cache(expire=60)
async def get_all_jobs(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
    limit: int = 100,
    skip: int = 0,
):
    return await crud_job.get_all(db=db, limit=limit, skip=skip)


@router.get(
    "/{job_uid}/",
    response_model=JobResponse,
    status_code=status.HTTP_200_OK,
)
async def get_job_by_uid(
    job_uid: UUID,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    found_job = await crud_job.get_by_uid(db=db, uid=job_uid)
    if not found_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job {job_uid} not found.",
        )

    return await crud_job.get_by_uid(db=db, uid=job_uid)


@router.post(
    "/",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_job(
    create_data: JobCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    try:
        uid = str(uuid.uuid4())
        new_job = await crud_job.create(
            db=db,
            create_schema=JobCreateDB(
                uid=uid,
                author_id=current_user.id,
                **create_data.model_dump(exclude_unset=True),
            ),
            commit=False,
        )
        await db.commit()
    except Exception as ex:
        await db.rollback()
        logger.exception(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the job.",
        ) from ex

    return new_job


@router.patch(
    "/author/{job_uid}/",
    response_model=JobResponse,
    status_code=status.HTTP_200_OK,
)
async def update_job_for_author(
    job_uid: UUID,
    update_data: JobUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    found_job = await crud_job.get_by_uid(db=db, uid=job_uid)
    if not found_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job {job_uid} not found.",
        )
    if found_job.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not permission to update this job",
        )

    return await crud_job.update(
        db=db,
        db_obj=found_job,
        update_data=update_data,
    )


@router.patch(
    "/admin/{job_uid}/",
    response_model=JobResponse,
    status_code=status.HTTP_200_OK,
)
async def update_job_for_admin(
    job_uid: UUID,
    update_data: JobUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    found_job = await crud_job.get_by_uid(db=db, uid=job_uid)
    if not found_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job {job_uid} not found.",
        )
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not permission to update this job",
        )

    return await crud_job.update(
        db=db,
        db_obj=found_job,
        update_data=update_data,
    )


@router.patch(
    "/performer/{job_uid}/",
    response_model=JobResponse,
    status_code=status.HTTP_200_OK,
)
async def update_job_for_performer(
    job_uid: UUID,
    update_data: JobUpdateForPerformer,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    found_job = await crud_job.get_by_uid(db=db, uid=job_uid)
    if not found_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job {job_uid} not found.",
        )
    if found_job.performer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not permission to update this job",
        )

    return await crud_job.update(
        db=db,
        db_obj=found_job,
        update_data=update_data,
    )


@router.delete("/{job_uid}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(
    job_uid: UUID,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    found_job = await crud_job.get_by_uid(db=db, uid=job_uid)
    if not found_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job {job_uid} not found.",
        )
    if found_job.author_id == current_user.id or current_user.is_admin:
        await crud_job.remove(db=db, obj_id=found_job.id)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not permission to delete this job",
        )
