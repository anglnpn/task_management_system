import string
import uuid
import random

from slugify import slugify
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user import UserCreateDB, UserCreate
from security.password import hash_password
from crud.user import crud_user
from models import User


async def create_user(
    db: AsyncSession,
    create_data: UserCreate,
) -> User:
    try:
        create_data_dict = create_data.model_dump(exclude_unset=True)
        hashed_password = await hash_password(create_data_dict.pop("password"))
        random_uid = str(uuid.uuid4())
        username = await generate_unique_username(
            db=db,
            first_name=create_data.first_name,
            second_name=create_data.second_name,
        )
        user_created = await crud_user.create(
            db=db,
            create_schema=UserCreateDB(
                uid=random_uid,
                username=username,
                hashed_password=hashed_password,
                **create_data_dict,
                commit=False,
            ),
        )
        await db.commit()
    except Exception:
        await db.rollback()
        raise

    return user_created


async def generate_unique_username(
    db: AsyncSession, first_name: str, second_name: str
) -> str:
    full_name = f"{first_name} {second_name}"
    username = slugify(full_name, separator="_")

    while True:
        if await crud_user.check_for_user(db=db, slug=username):
            return username

        random_chars = "".join(
            random.choices(string.ascii_lowercase + string.digits, k=3)  # noqa: S311
        )
        username = f"{username}_{random_chars}"
