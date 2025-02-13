from typing import Callable
from uuid import uuid4

from httpx import AsyncClient

from models import User
from schemas.user import UserUpdateDB, UserCreate, UserUpdateFullDB

ROOT_ENDPOINT = "/api/v1/user/"


class TestUser:
    async def test_get_user_account(
        self,
        http_client: AsyncClient,
        user_fixture: User,
        get_auth_headers: Callable,
    ):
        user_auth_headers = await get_auth_headers(user_fixture)

        response = await http_client.get(
            ROOT_ENDPOINT, headers=user_auth_headers
        )
        response_data = response.json()
        assert response.status_code == 200
        assert response_data["id"] == user_fixture.id

    async def test_get_user_by_uid(
        self,
        http_client: AsyncClient,
        user_fixture: User,
        user_fixture_2: User,
        get_auth_headers: Callable,
    ):
        endpoint = f"{ROOT_ENDPOINT}{user_fixture.uid}/"
        user_auth_headers = await get_auth_headers(user_fixture)

        response = await http_client.get(endpoint, headers=user_auth_headers)
        response_data = response.json()
        assert response.status_code == 200
        assert response_data["id"] == user_fixture.id

    async def test_get_users_all(
        self,
        http_client: AsyncClient,
        user_fixture: User,
        user_fixture_2: User,
        get_auth_headers: Callable,
    ):
        endpoint = f"{ROOT_ENDPOINT}all/"
        user_auth_headers = await get_auth_headers(user_fixture)

        response = await http_client.get(endpoint, headers=user_auth_headers)
        assert response.status_code == 200

    async def test_create_user(
        self,
        http_client: AsyncClient,
        user_fixture: User,
        user_fixture_2: User,
        get_auth_headers: Callable,
    ):
        update_schema = UserCreate(
            first_name="user",
            second_name="user",
            email="test4@gmail.com",
            password="testtest",
        )
        response = await http_client.post(
            ROOT_ENDPOINT, json=update_schema.model_dump()
        )
        assert response.status_code == 201

        response_data = response.json()
        assert response_data["first_name"] == "user"

    async def test_update_user_account(
        self,
        http_client: AsyncClient,
        user_fixture: User,
        get_auth_headers: Callable,
    ):
        user_auth_headers = await get_auth_headers(user_fixture)
        update_schema = UserUpdateDB(first_name="for test")
        response = await http_client.patch(
            ROOT_ENDPOINT,
            json=update_schema.model_dump(),
            headers=user_auth_headers,
        )
        assert response.status_code == 200

        response_data = response.json()
        assert response_data["first_name"] == "for test"

    async def test_update_user_by_admin(
        self,
        http_client: AsyncClient,
        user_fixture: User,
        user_fixture_3: User,
        get_auth_headers: Callable,
    ):
        user_auth_headers = await get_auth_headers(user_fixture_3)
        endpoint = f"{ROOT_ENDPOINT}{user_fixture.uid}/"
        update_schema = UserUpdateFullDB(is_deleted=True)
        response = await http_client.patch(
            endpoint,
            json=update_schema.model_dump(),
            headers=user_auth_headers,
        )
        assert response.status_code == 200

        response_data = response.json()
        assert response_data["is_deleted"] is True

    async def test_delete_user(
        self,
        http_client: AsyncClient,
        user_fixture: User,
        get_auth_headers: Callable,
    ):
        endpoint = f"{ROOT_ENDPOINT}{user_fixture.uid}/"
        user_auth_headers = await get_auth_headers(user_fixture)
        response = await http_client.delete(
            endpoint, headers=user_auth_headers
        )
        assert response.status_code == 204

    async def test_delete_user_with_wrong_uid(
        self,
        http_client: AsyncClient,
        user_fixture: User,
        get_auth_headers: Callable,
    ):
        test_uid = uuid4()
        endpoint = f"{ROOT_ENDPOINT}{test_uid}/"
        user_auth_headers = await get_auth_headers(user_fixture)
        response = await http_client.delete(
            endpoint, headers=user_auth_headers
        )
        assert response.status_code == 404

    async def test_delete_user_by_unauthorized(
        self,
        http_client: AsyncClient,
        user_fixture_2: User,
        user_fixture: User,
        get_auth_headers: Callable,
    ):
        endpoint = f"{ROOT_ENDPOINT}{user_fixture.uid}/"
        user_auth_headers = await get_auth_headers(user_fixture_2)
        response = await http_client.delete(
            endpoint, headers=user_auth_headers
        )
        assert response.status_code == 403
