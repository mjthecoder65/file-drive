import pytest

from faker import Faker
from fastapi import status
from pydantic import BaseModel
from fastapi.testclient import TestClient
from configs.settings import settings
from main import app

client = TestClient(app)


class UserIn(BaseModel):
    username: str
    email: str
    password: str


def get_random_user():
    faker = Faker()
    username = faker.user_name()
    email = faker.email()
    password = faker.password()

    return UserIn(username=username, email=email, password=password)


@pytest.mark.integration
class TestAuth:
    @pytest.mark.asyncio
    async def test_register(self):
        new_user = get_random_user()
        payload = {
            "username": new_user.username,
            "email": new_user.email,
            "password": new_user.password,
        }
        response = client.post(
            f"{settings.API_ENDPOINT_PREFIX}/auth/register", json=payload
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["access_token"] is not None
        assert response.json()["token_type"] == "bearer"
