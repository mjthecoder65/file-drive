from contextlib import asynccontextmanager
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from configs.settings import settings
from configs.database import Base

engine = create_async_engine(settings.DATABASE_URL_TEST, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


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
