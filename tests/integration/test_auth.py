import pytest
from faker import Faker
from fastapi import status
from httpx import AsyncClient
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from configs.database import get_session
from configs.settings import settings
from main import app

engine = create_async_engine(settings.DATABASE_URL_TEST, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


app.dependency_overrides[get_session] = get_db


class UserIn(BaseModel):
    username: str
    email: str
    password: str


def get_random_user():
    faker = Faker()
    username = faker.username()  # specify length of username.
    email = faker.email()
    password = faker.password(length=10)

    return UserIn(username=username, email=email, password=password)


@pytest.mark.integration
class TestAuth:
    @pytest.mark.anyio
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
