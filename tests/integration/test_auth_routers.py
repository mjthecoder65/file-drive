import pytest
from faker import Faker
from fastapi import status
from httpx import AsyncClient

from configs.settings import settings
from tests.common import get_random_user

faker = Faker()


@pytest.mark.integration
class TestAuth:
    async def test_register(self, client: AsyncClient):
        new_user = get_random_user()
        payload = {
            "username": new_user.username,
            "email": new_user.email,
            "password": new_user.password,
        }
        response = await client.post(
            f"{settings.API_ENDPOINT_PREFIX}/auth/register", json=payload
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["access_token"] is not None
        assert response.json()["token_type"] == "bearer"

    async def test_register_existing_user(self, client: AsyncClient):
        new_user = get_random_user()
        payload = {
            "username": new_user.username,
            "email": new_user.email,
            "password": new_user.password,
        }

        await client.post(f"{settings.API_ENDPOINT_PREFIX}/auth/register", json=payload)

        response = await client.post(
            f"{settings.API_ENDPOINT_PREFIX}/auth/register", json=payload
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["detail"] == "User with this email already exists"

    async def test_login(self, client: AsyncClient):
        new_user = get_random_user()
        payload = {
            "username": new_user.username,
            "email": new_user.email,
            "password": new_user.password,
        }
        await client.post(f"{settings.API_ENDPOINT_PREFIX}/auth/register", json=payload)

        response = await client.post(
            f"{settings.API_ENDPOINT_PREFIX}/auth/login",
            data={"username": new_user.email, "password": new_user.password},
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["access_token"] is not None
        assert response.json()["token_type"] == "bearer"

    async def test_login_wrong_email(self, client: AsyncClient):
        new_user = get_random_user()
        payload = {
            "username": new_user.username,
            "email": new_user.email,
            "password": new_user.password,
        }
        await client.post(f"{settings.API_ENDPOINT_PREFIX}/auth/register", json=payload)

        response = await client.post(
            f"{settings.API_ENDPOINT_PREFIX}/auth/login",
            data={"username": faker.email(), "password": new_user.password},
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["detail"] == "Wrong email or password"

    async def test_login_wrong_password(self, client: AsyncClient):
        new_user = get_random_user()
        payload = {
            "username": new_user.username,
            "email": new_user.email,
            "password": new_user.password,
        }
        await client.post(f"{settings.API_ENDPOINT_PREFIX}/auth/register", json=payload)

        response = await client.post(
            f"{settings.API_ENDPOINT_PREFIX}/auth/login",
            data={"username": new_user.email, "password": faker.password()},
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["detail"] == "Wrong email or password"
