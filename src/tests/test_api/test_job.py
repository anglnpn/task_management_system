from typing import Callable
from uuid import uuid4

from httpx import AsyncClient

from models import Job, User
from schemas.job import JobCreate, JobUpdate, JobUpdateForPerformer

ROOT_ENDPOINT = "/api/v1/job/"


class TestJob:
    async def test_get_all_jobs(
        self,
        http_client: AsyncClient,
        job_fixture: Job,
        job_fixture_2: Job,
        user_fixture: User,
        get_auth_headers: Callable,
    ):
        endpoint = ROOT_ENDPOINT + "all/"
        user_auth_headers = await get_auth_headers(user_fixture)

        response = await http_client.get(endpoint, headers=user_auth_headers)

        assert response.status_code == 200
        assert len(response.json()) == 2

    async def test_get_job_by_uid(
        self,
        http_client: AsyncClient,
        job_fixture: Job,
        user_fixture: User,
        get_auth_headers: Callable,
    ):
        endpoint = f"{ROOT_ENDPOINT}{job_fixture.uid}/"
        user_auth_headers = await get_auth_headers(user_fixture)

        response = await http_client.get(endpoint, headers=user_auth_headers)
        response_data = response.json()
        assert response.status_code == 200
        assert response_data["uid"] == str(job_fixture.uid)

    async def test_get_job_by_wrong_uid(
        self,
        http_client: AsyncClient,
        job_fixture: Job,
        user_fixture: User,
        get_auth_headers: Callable,
    ):
        test_uid = uuid4()
        endpoint = f"{ROOT_ENDPOINT}{test_uid!s}/"
        user_auth_headers = await get_auth_headers(user_fixture)

        response = await http_client.get(endpoint, headers=user_auth_headers)
        assert response.status_code == 404

    async def test_get_jobs_by_author(
        self,
        http_client: AsyncClient,
        job_fixture: Job,
        job_fixture_2: Job,
        user_fixture: User,
        get_auth_headers: Callable,
    ):
        endpoint = f"{ROOT_ENDPOINT}author/"
        user_auth_headers = await get_auth_headers(user_fixture)

        response = await http_client.get(endpoint, headers=user_auth_headers)
        assert response.status_code == 200
        assert len(response.json()) == 2

    async def test_get_jobs_by_performer(
        self,
        http_client: AsyncClient,
        job_fixture: Job,
        job_fixture_2: Job,
        user_fixture_2: User,
        get_auth_headers: Callable,
    ):
        endpoint = f"{ROOT_ENDPOINT}performer/"
        user_auth_headers = await get_auth_headers(user_fixture_2)

        response = await http_client.get(endpoint, headers=user_auth_headers)
        assert response.status_code == 200
        assert len(response.json()) == 2

    async def test_create_job(
        self,
        http_client: AsyncClient,
        user_fixture: User,
        user_fixture_2: User,
        get_auth_headers: Callable,
    ):
        user_auth_headers = await get_auth_headers(user_fixture)
        new_job_schema = JobCreate(
            title="test", description="test", performer_id=user_fixture_2.id
        )
        response = await http_client.post(
            ROOT_ENDPOINT,
            json=new_job_schema.model_dump(),
            headers=user_auth_headers,
        )
        assert response.status_code == 201

        response_data = response.json()
        assert response_data["title"] == "test"

    async def test_update_job_by_author(
        self,
        http_client: AsyncClient,
        job_fixture: Job,
        job_fixture_2: Job,
        user_fixture: User,
        get_auth_headers: Callable,
    ):
        endpoint = f"{ROOT_ENDPOINT}author/{job_fixture.uid}/"
        user_auth_headers = await get_auth_headers(user_fixture)
        update_schema = JobUpdate(title="for test")
        response = await http_client.patch(
            endpoint,
            json=update_schema.model_dump(),
            headers=user_auth_headers,
        )
        assert response.status_code == 200

        response_data = response.json()
        assert response_data["title"] == "for test"

    async def test_update_job_by_admin(
        self,
        http_client: AsyncClient,
        job_fixture: Job,
        job_fixture_2: Job,
        user_fixture_3: User,
        get_auth_headers: Callable,
    ):
        endpoint = f"{ROOT_ENDPOINT}admin/{job_fixture.uid}/"
        user_auth_headers = await get_auth_headers(user_fixture_3)
        update_schema = JobUpdate(title="for test")
        response = await http_client.patch(
            endpoint,
            json=update_schema.model_dump(),
            headers=user_auth_headers,
        )
        assert response.status_code == 200

        response_data = response.json()
        assert response_data["title"] == "for test"

    async def test_update_author_job_by_unauthorized(
        self,
        http_client: AsyncClient,
        job_fixture: Job,
        job_fixture_2: Job,
        user_fixture_2: User,
        get_auth_headers: Callable,
    ):
        endpoint = f"{ROOT_ENDPOINT}{job_fixture.uid}/"
        user_auth_headers = await get_auth_headers(user_fixture_2)
        update_schema = JobUpdate(title="for test")
        response = await http_client.patch(
            endpoint,
            json=update_schema.model_dump(),
            headers=user_auth_headers,
        )
        assert response.status_code == 405

    async def test_update_job_by_performer(
        self,
        http_client: AsyncClient,
        job_fixture: Job,
        job_fixture_2: Job,
        user_fixture_2: User,
        get_auth_headers: Callable,
    ):
        endpoint = f"{ROOT_ENDPOINT}performer/{job_fixture.uid}/"
        user_auth_headers = await get_auth_headers(user_fixture_2)
        update_schema = JobUpdateForPerformer(is_completed=True)
        response = await http_client.patch(
            endpoint,
            json=update_schema.model_dump(),
            headers=user_auth_headers,
        )
        assert response.status_code == 200

    async def test_update_performer_job_by_unauthorized(
        self,
        http_client: AsyncClient,
        job_fixture: Job,
        job_fixture_2: Job,
        user_fixture: User,
        get_auth_headers: Callable,
    ):
        endpoint = f"{ROOT_ENDPOINT}performer/{job_fixture.uid}/"
        user_auth_headers = await get_auth_headers(user_fixture)
        update_schema = JobUpdateForPerformer(is_completed=True)
        response = await http_client.patch(
            endpoint,
            json=update_schema.model_dump(),
            headers=user_auth_headers,
        )
        assert response.status_code == 403

    async def test_delete_job(
        self,
        http_client: AsyncClient,
        job_fixture: Job,
        user_fixture: User,
        get_auth_headers: Callable,
    ):
        endpoint = f"{ROOT_ENDPOINT}{job_fixture.uid}/"
        user_auth_headers = await get_auth_headers(user_fixture)
        response = await http_client.delete(
            endpoint, headers=user_auth_headers
        )
        assert response.status_code == 204

    async def test_delete_job_with_wrong_uid(
        self,
        http_client: AsyncClient,
        job_fixture: Job,
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

    async def test_delete_job_by_unauthorized(
        self,
        http_client: AsyncClient,
        job_fixture: Job,
        user_fixture_2: User,
        get_auth_headers: Callable,
    ):
        endpoint = f"{ROOT_ENDPOINT}{job_fixture.uid}/"
        user_auth_headers = await get_auth_headers(user_fixture_2)
        response = await http_client.delete(
            endpoint, headers=user_auth_headers
        )
        assert response.status_code == 403
