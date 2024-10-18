import pytest
from fastapi import status
from httpx import AsyncClient

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

    async def test_get_me_invalid_token(self, client: AsyncClient):
        pass
