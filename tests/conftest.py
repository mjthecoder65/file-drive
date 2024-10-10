from contextlib import asynccontextmanager

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from configs.database import Base, get_session
from configs.settings import settings
from main import app

engine = create_async_engine(settings.DATABASE_URL_TEST, echo=False)

AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


app.dependency_overrides[get_session] = get_db


@pytest.fixture(scope="function", autouse=True)
async def client():
    async with AsyncClient(
        base_url="http://test", transport=ASGITransport(app=app)
    ) as client:
        yield client


@asynccontextmanager
async def get_session():
    async with AsyncSessionLocal() as session:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield session
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function", autouse=True)
async def db():
    async with get_session() as session:
        yield session
