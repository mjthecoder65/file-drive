import random
import uuid
from datetime import datetime, timedelta, timezone
from unittest import mock
from unittest.mock import AsyncMock

import pytest
from faker import Faker
from fastapi import status
from httpx import AsyncClient

from auth.auth import create_access_token, decode_access_token
from configs.settings import settings
from models.user import User
from services.file import FileService
from services.user import UserService
from tests.common import get_random_user


@pytest.fixture(scope="function")
async def admin_user(user_service: UserService) -> User:
    new_user = get_random_user()
    return await user_service.register(
        username=new_user.username,
        email=new_user.email,
        password=new_user.password,
        is_admin=True,
    )


@pytest.fixture(scope="function")
def mock_file_service():
    mock_file_service = AsyncMock(spec=FileService)
    return mock_file_service


@pytest.mark.integration
class TestUserRouters:
    async def test_get_me(self, client: AsyncClient):
        new_user = get_random_user()
        payload = {
            "username": new_user.username,
            "email": new_user.email,
            "password": new_user.password,
        }

        res = await client.post(
            f"{settings.API_ENDPOINT_PREFIX}/auth/register", json=payload
        )

        assert res.status_code == status.HTTP_201_CREATED

        res = await client.post(
            f"{settings.API_ENDPOINT_PREFIX}/auth/login",
            data={"username": new_user.email, "password": new_user.password},
        )
        assert res.status_code == status.HTTP_200_OK
        access_token = res.json()["access_token"]
        assert access_token is not None
        assert type(access_token) == str

        res = await client.get(
            f"{settings.API_ENDPOINT_PREFIX}/users/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert res.status_code == status.HTTP_200_OK
        assert res.json()["username"] == new_user.username
        assert res.json()["email"] == new_user.email

    async def test_get_me_unauthorized(self, client: AsyncClient):
        res = await client.get(f"{settings.API_ENDPOINT_PREFIX}/users/me")
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_get_me_with_expired_token(
        self, client: AsyncClient, user_service: UserService
    ):
        new_user = get_random_user()
        user = await user_service.register(
            username=new_user.username, email=new_user.email, password=new_user.password
        )

        access_token = create_access_token(
            user.id,
            is_admin=user.is_admin,
            expires_datetime=datetime.now(tz=timezone.utc) - timedelta(hours=1),
        )

        res = await client.get(
            f"{settings.API_ENDPOINT_PREFIX}/users/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_get_all_users(
        self, client: AsyncClient, user_service: UserService, admin_user: User
    ):

        for _ in range(10):
            new_user = get_random_user()
            payload = {
                "username": new_user.username,
                "email": new_user.email,
                "password": new_user.password,
            }

            res = await client.post(
                f"{settings.API_ENDPOINT_PREFIX}/auth/register", json=payload
            )
            assert res.status_code == status.HTTP_201_CREATED

        access_token = create_access_token(
            id=admin_user.id,
            is_admin=admin_user.is_admin,
            expires_datetime=datetime.now(tz=timezone.utc) + timedelta(hours=2),
        )

        params = {"limit": 5, "offset": 0}

        res = await client.get(
            f"{settings.API_ENDPOINT_PREFIX}/users",
            headers={"Authorization": f"Bearer {access_token}"},
            params=params,
        )

        assert res.status_code == status.HTTP_200_OK
        payload = res.json()
        assert payload["total"] == 11
        assert len(payload["data"]) == 5
        assert payload["limit"] == 5
        assert payload["offset"] == 0

    async def test_get_all_users_unauthorized(self, client: AsyncClient):
        res = await client.get(f"{settings.API_ENDPOINT_PREFIX}/users")
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_get_all_users_not_admin(self, client: AsyncClient):
        new_user = get_random_user()
        res = await client.post(
            f"{settings.API_ENDPOINT_PREFIX}/auth/register",
            json={
                "username": new_user.username,
                "email": new_user.email,
                "password": new_user.password,
            },
        )

        assert res.status_code == status.HTTP_201_CREATED
        assert res.json()["access_token"] is not None
        assert res.json()["token_type"] == "bearer"

        access_token = res.json()["access_token"]

        res = await client.get(
            f"{settings.API_ENDPOINT_PREFIX}/users",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert res.status_code == status.HTTP_403_FORBIDDEN

    async def test_get_user_files(self, client: AsyncClient, mock_file_service):
        new_user = get_random_user()
        payload = {
            "username": new_user.username,
            "email": new_user.email,
            "password": new_user.password,
        }

        res = await client.post(
            f"{settings.API_ENDPOINT_PREFIX}/auth/register", json=payload
        )

        assert res.status_code == status.HTTP_201_CREATED

        access_token = res.json()["access_token"]
        user_id = decode_access_token(access_token)["sub"]

        mock_file_service.get_files_by_user_id.return_value = [
            {
                "id": str(uuid.uuid4()),
                "name": "test_file",
                "extension": "txt",
                "mime_type": "text/plain",
                "size": 1024,
                "url": "http://test.com",
                "created_at": datetime.now(tz=timezone.utc),
                "updated_at": datetime.now(tz=timezone.utc),
            }
        ]

        mock_file_service.get_files_count_by_user_id.return_value = 1

        with mock.patch(
            "routers.users.FileService", return_value=mock_file_service
        ) as mock_file_service:
            res = await client.get(
                f"{settings.API_ENDPOINT_PREFIX}/users/{user_id}/files",
                headers={"Authorization": f"Bearer {access_token}"},
            )

            assert res.status_code == status.HTTP_200_OK
            assert len(res.json()["data"]) == 1

    async def test_get_user_by_id(self, client: AsyncClient, admin_user: User):
        new_user = get_random_user()
        payload = {
            "username": new_user.username,
            "email": new_user.email,
            "password": new_user.password,
        }

        res = await client.post(
            f"{settings.API_ENDPOINT_PREFIX}/auth/register", json=payload
        )
        assert res.status_code == status.HTTP_201_CREATED

        user_id = decode_access_token(res.json()["access_token"])["sub"]

        access_token = create_access_token(
            id=admin_user.id,
            is_admin=admin_user.is_admin,
            expires_datetime=datetime.now(tz=timezone.utc) + timedelta(hours=2),
        )

        res = await client.get(
            f"{settings.API_ENDPOINT_PREFIX}/users/{user_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert res.status_code == status.HTTP_200_OK
        assert res.json()["username"] == new_user.username
        assert res.json()["email"] == new_user.email
        assert res.json()["id"] == user_id

    async def test_get_user_by_id_unauthorized(self, client: AsyncClient):
        res = await client.get(f"{settings.API_ENDPOINT_PREFIX}/users/123")
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_get_user_by_id_not_admin(self, client: AsyncClient):
        new_user = get_random_user()
        res = await client.post(
            f"{settings.API_ENDPOINT_PREFIX}/auth/register",
            json={
                "username": new_user.username,
                "email": new_user.email,
                "password": new_user.password,
            },
        )

        assert res.status_code == status.HTTP_201_CREATED
        assert res.json()["access_token"] is not None
        assert res.json()["token_type"] == "bearer"

        access_token = res.json()["access_token"]

        res = await client.get(
            f"{settings.API_ENDPOINT_PREFIX}/users/123",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert res.status_code == status.HTTP_403_FORBIDDEN

    async def test_change_password(self, client: AsyncClient):
        new_user = get_random_user()
        payload = {
            "username": new_user.username,
            "email": new_user.email,
            "password": new_user.password,
        }

        res = await client.post(
            f"{settings.API_ENDPOINT_PREFIX}/auth/register", json=payload
        )
        assert res.status_code == status.HTTP_201_CREATED

        access_token = res.json()["access_token"]

        user_id = decode_access_token(access_token)["sub"]
        faker = Faker()

        res = await client.put(
            f"{settings.API_ENDPOINT_PREFIX}/users/{user_id}/change-password",
            headers={"Authorization": f"Bearer {access_token}"},
            json={
                "old_password": new_user.password,
                "new_password": faker.password(length=random.randint(8, 256)),
            },
        )

        assert res.status_code == status.HTTP_200_OK

    async def test_change_password_wrong_old_password(self, client: AsyncClient):
        new_user = get_random_user()
        payload = {
            "username": new_user.username,
            "email": new_user.email,
            "password": new_user.password,
        }

        res = await client.post(
            f"{settings.API_ENDPOINT_PREFIX}/auth/register", json=payload
        )
        assert res.status_code == status.HTTP_201_CREATED

        access_token = res.json()["access_token"]
        user_id = decode_access_token(access_token)["sub"]

        faker = Faker()
        res = await client.put(
            f"{settings.API_ENDPOINT_PREFIX}/users/{user_id}/change-password",
            headers={"Authorization": f"Bearer {access_token}"},
            json={
                "old_password": faker.password(length=random.randint(8, 256)),
                "new_password": faker.password(length=random.randint(8, 256)),
            },
        )

        assert res.status_code == status.HTTP_400_BAD_REQUEST

    async def test_change_password_wrong_user_id(self, client: AsyncClient):
        new_user = get_random_user()
        payload = {
            "username": new_user.username,
            "email": new_user.email,
            "password": new_user.password,
        }

        res = await client.post(
            f"{settings.API_ENDPOINT_PREFIX}/auth/register", json=payload
        )
        assert res.status_code == status.HTTP_201_CREATED

        access_token = res.json()["access_token"]

        faker = Faker()
        user_id = uuid.uuid4()

        res = await client.put(
            f"{settings.API_ENDPOINT_PREFIX}/users/{user_id}/change-password",
            headers={"Authorization": f"Bearer {access_token}"},
            json={
                "old_password": new_user.password,
                "new_password": faker.password(length=random.randint(8, 256)),
            },
        )

        assert res.status_code == status.HTTP_403_FORBIDDEN

    async def test_delete_user(self, client: AsyncClient):
        new_user = get_random_user()
        payload = {
            "username": new_user.username,
            "email": new_user.email,
            "password": new_user.password,
        }

        res = await client.post(
            f"{settings.API_ENDPOINT_PREFIX}/auth/register", json=payload
        )
        assert res.status_code == status.HTTP_201_CREATED

        access_token = res.json()["access_token"]
        user_id = decode_access_token(access_token)["sub"]

        res = await client.delete(
            f"{settings.API_ENDPOINT_PREFIX}/users/{user_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert res.status_code == status.HTTP_204_NO_CONTENT

    async def test_delete_user_wrong_user_id(self, client: AsyncClient):
        new_user = get_random_user()
        payload = {
            "username": new_user.username,
            "email": new_user.email,
            "password": new_user.password,
        }

        res = await client.post(
            f"{settings.API_ENDPOINT_PREFIX}/auth/register", json=payload
        )
        assert res.status_code == status.HTTP_201_CREATED

        access_token = res.json()["access_token"]

        user_id = uuid.uuid4()

        res = await client.delete(
            f"{settings.API_ENDPOINT_PREFIX}/users/{user_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert res.status_code == status.HTTP_403_FORBIDDEN
