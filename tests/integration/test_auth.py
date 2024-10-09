import pytest

from faker import Faker
from pydantic import BaseModel
from fastapi.testclient import TestClient
from configs.settings import settings
from main import app

client = TestClient(app)

# Overrid dependencies


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
        pass
