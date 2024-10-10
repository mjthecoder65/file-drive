import pytest
from fastapi import status
from httpx import AsyncClient

from auth.auth import create_access_token
from configs.settings import settings
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

        res = await client.get(
            f"{settings.API_ENDPOINT_PREFIX}/users/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )

    async def test_get_me_unauthorized(self, client: AsyncClient):
        res = await client.get(f"{settings.API_ENDPOINT_PREFIX}/users/me")
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_get_me_invalid_token(self, client: AsyncClient):
        pass
