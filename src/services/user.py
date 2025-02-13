import uuid
from typing import Union

from slugify import slugify
from sqlalchemy.ext.asyncio import AsyncSession

from configs.config import admin_settings
from configs.loggers import logger
from schemas.user import (
    UserCreateDB,
    UserCreate,
    AdminCreateDB,
    UserUpdateFullDB,
    UserUpdateDB,
)
from security.password import hash_password
from crud.user import crud_user
from models import User
from utilities.exceptions import UserNameExistError


async def create_user(
    db: AsyncSession,
    create_data: UserCreate,
) -> User:
    try:
        create_data_dict = create_data.model_dump(exclude_unset=True)
        hashed_password = await hash_password(create_data_dict.pop("password"))
        username = await generate_unique_username(
            db=db,
            first_name=create_data.first_name,
            second_name=create_data.second_name,
        )
        user_created = await crud_user.create(
            db=db,
            create_schema=UserCreateDB(
                uid=str(uuid.uuid4()),
                username=username,
                hashed_password=hashed_password,
                **create_data_dict,
            ),
            commit=False,
        )
        await db.commit()
    except Exception as ex:
        await db.rollback()
        logger.exception(ex)
        raise

    return user_created


async def create_admin(db: AsyncSession) -> User:
    try:
        hashed_password = await hash_password(admin_settings.ADMIN_PASSWORD)
        user_created = await crud_user.create(
            db=db,
            create_schema=AdminCreateDB(
                uid=str(uuid.uuid4()),
                first_name=admin_settings.ADMIN_FIRST_NAME,
                second_name=admin_settings.ADMIN_SECOND_NAME,
                username=admin_settings.ADMIN_USERNAME,
                hashed_password=hashed_password,
                email=admin_settings.ADMIN_EMAIL,
                is_admin=True,
            ),
            commit=False,
        )
        await db.commit()
    except Exception as ex:
        await db.rollback()
        logger.exception(ex)
        raise

    return user_created


async def update_user(
    db: AsyncSession,
    found_user: User,
    update_data: Union[UserUpdateFullDB, UserUpdateDB],
) -> User:
    try:
        if (
            update_data.username
            and update_data.username != found_user.username
            and await crud_user.check_for_user(
                db=db, slug=update_data.username
            )
        ):
            ex = "Username already exists."
            raise UserNameExistError(ex)  # noqa: TRY301

        updated_user = await crud_user.update(
            db=db,
            db_obj=found_user,
            update_data=update_data,
            commit=False,
        )
        await db.commit()
    except UserNameExistError as ex:
        await db.rollback()
        logger.exception(ex)
        raise
    except Exception as ex:
        await db.rollback()
        logger.exception(ex)
        raise

    return updated_user


async def generate_unique_username(
    db: AsyncSession, first_name: str, second_name: str
) -> str:
    full_name = f"{first_name} {second_name}"
    username = slugify(full_name, separator="_")

    if not await crud_user.check_for_user(db=db, slug=username):
        return username

    unique_id = uuid.uuid4().hex[:6]
    return f"{username}_{unique_id}"
