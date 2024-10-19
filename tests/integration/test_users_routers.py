from datetime import datetime, timedelta, timezone

import pytest
from fastapi import status
from httpx import AsyncClient

from auth.auth import create_access_token
from configs.settings import settings
from services.user import UserService
from tests.common import get_random_user


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

    async def test_get_all_users(self, client: AsyncClient, user_service: UserService):

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

        new_user = get_random_user()
        admin_user = await user_service.register(
            username=new_user.username,
            email=new_user.email,
            password=new_user.password,
            is_admin=True,
        )

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
