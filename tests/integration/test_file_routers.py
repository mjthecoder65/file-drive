import io
import uuid
from datetime import datetime, timedelta, timezone
from unittest import mock

import pytest
from faker import Faker
from fastapi import status
from httpx import AsyncClient

from auth.auth import create_access_token
from configs.settings import settings
from services.file import FileService
from services.user import UserService
from tests.common import get_random_user


@pytest.mark.integration
async def test_upload_file(client: AsyncClient):
    new_user = get_random_user()
    payload = {
        "username": new_user.username,
        "password": new_user.password,
        "email": new_user.email,
    }

    res = await client.post(
        f"{settings.API_ENDPOINT_PREFIX}/auth/register", json=payload
    )
    assert res.status_code == status.HTTP_201_CREATED
    assert res.json()["access_token"] is not None

    faker = Faker()
    access_token = res.json()["access_token"]
    file_stream = io.BytesIO(b"Sample file data")
    file_name = faker.name()
    file = {"file": (file_name, file_stream, "text/plain")}

    fake_signed_url = faker.url(schemes=["https"])
    with mock.patch.object(
        FileService, "_upload_to_gcs", return_value=None
    ) as _upload_to_gcs, mock.patch.object(
        FileService, "_generate_signed_url", return_value=fake_signed_url
    ) as _generate_signed_url:
        res = await client.post(
            f"{settings.API_ENDPOINT_PREFIX}/files",
            files=file,
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert res.status_code == status.HTTP_200_OK
        assert _upload_to_gcs.called
        assert _generate_signed_url.called
        assert file_name in res.json()["name"]
        assert fake_signed_url in res.json()["url"]


@pytest.mark.integration
async def test_get_file_by_id(client: AsyncClient, user_service: UserService):
    new_user = get_random_user()
    admin_user = await user_service.register(
        username=new_user.username,
        password=new_user.password,
        email=new_user.email,
        is_admin=True,
    )

    access_token = create_access_token(
        id=admin_user.id,
        is_admin=admin_user.is_admin,
        expires_datetime=datetime.now(timezone.utc) + timedelta(days=1),
    )

    faker = Faker()
    file_stream = io.BytesIO(b"Sample file data")
    file_name = faker.name()
    file = {"file": (file_name, file_stream, "text/plain")}

    with mock.patch.object(
        FileService, "_upload_to_gcs", return_value=None
    ) as _upload_to_gcs, mock.patch.object(
        FileService, "_generate_signed_url", return_value=faker.url(schemes=["https"])
    ) as _generate_signed_url:
        res = await client.post(
            f"{settings.API_ENDPOINT_PREFIX}/files",
            files=file,
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert res.status_code == status.HTTP_200_OK
        assert _upload_to_gcs.called
        assert _generate_signed_url.called

        file_id = res.json()["id"]

        res = await client.get(
            f"{settings.API_ENDPOINT_PREFIX}/files/{file_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert res.status_code == status.HTTP_200_OK
        assert file_name in res.json()["name"]
        assert file_id == res.json()["id"]


@pytest.mark.integration
async def test_get_file_by_id_not_admin(client: AsyncClient):
    new_user = get_random_user()
    payload = {
        "username": new_user.username,
        "password": new_user.password,
        "email": new_user.email,
    }

    res = await client.post(
        f"{settings.API_ENDPOINT_PREFIX}/auth/register", json=payload
    )
    assert res.status_code == status.HTTP_201_CREATED
    assert res.json()["access_token"] is not None

    access_token = res.json()["access_token"]

    res = await client.get(
        f"{settings.API_ENDPOINT_PREFIX}/files/{uuid.uuid4()}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert res.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.integration
async def test_delete_file_by_id(client: AsyncClient, user_service: UserService):
    pass
