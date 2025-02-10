from typing import Union

from jose import jwt
from pydantic import ValidationError
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from configs.config import jwt_settings
from crud.user import crud_user
from databases.database import get_async_session
from security.password import verify_password
from utilities.tokens import TokenSubject, create_tokens


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form.get("username"), form.get("password")
        async for db in get_async_session():
            found_user = await crud_user.get_by_username(db, username=username)
            if not found_user:
                return False
            if (
                await verify_password(
                    plain_password=password,
                    hashed_password=found_user.hashed_password,
                )
                and found_user.is_admin
            ):
                subject = TokenSubject(uid=str(found_user.uid))
                token = await create_tokens(subject)
                request.session.update({"token": token.access_token})
                return True

        return False

    async def logout(self, request: Request) -> RedirectResponse:
        request.session.clear()
        return RedirectResponse("/admin/login")

    async def authenticate(
        self, request: Request
    ) -> Union[bool, RedirectResponse]:
        token = request.session.get("token")
        if not token:
            return RedirectResponse("/admin/login")
        try:
            user_uid = jwt.decode(
                token, jwt_settings.JWT_SECRET_KEY, jwt_settings.JWT_ALGORITHM
            )
            if user_uid is None:
                return RedirectResponse("/admin/login")
        except (jwt.JWTError, ValidationError):
            return RedirectResponse("/admin/login")
        return True
