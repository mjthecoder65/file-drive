import io
from unittest import mock

import pytest
from fastapi import status
from httpx import AsyncClient

from configs.settings import settings
from services.file import FileService
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

    access_token = res.json()["access_token"]
    file_stream = io.BytesIO(b"Sample file data")
    file_name = "sample.txt"
    file = {"file": (file_name, file_stream, "text/plain")}

    with mock.patch.object(
        FileService, "_upload_to_gcs", return_value=None
    ) as _upload_to_gcs, mock.patch.object(
        FileService, "_generate_signed_url", return_value="http://mockurl.com"
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
        assert "http://mockurl.com" in res.json()["url"]
