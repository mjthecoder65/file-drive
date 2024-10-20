import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.integration
async def test_health_check(client: AsyncClient):
    res = await client.get("/health")

    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {"status": "ok"}


@pytest.mark.integration
async def test_readiness_check(client: AsyncClient):
    res = await client.get("/readiness")

    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {"status": "ok"}
