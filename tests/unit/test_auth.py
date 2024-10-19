import uuid
from datetime import datetime, timedelta, timezone

import pytest
from faker import Faker
from jose import ExpiredSignatureError, jwt

from auth.auth import create_access_token, decode_access_token

faker = Faker()


def test_create_access_token_no_expiration():
    is_admin = faker.boolean()
    access_token = create_access_token(
        uuid.uuid4(),
        is_admin=is_admin,
        expires_datetime=datetime.now(tz=timezone.utc) + timedelta(hours=2),
    )
    assert access_token is not None
    assert isinstance(access_token, str)
    assert access_token != ""

    payload = decode_access_token(access_token)

    assert payload is not None
    assert isinstance(payload, dict)
    assert payload["is_admin"] == is_admin


def test_create_access_token_with_expiration():
    is_admin = faker.boolean()
    access_token = create_access_token(
        uuid.uuid4(),
        is_admin=is_admin,
        expires_datetime=datetime.now(tz=timezone.utc) - timedelta(hours=2),
    )

    assert access_token is not None
    assert isinstance(access_token, str)

    with pytest.raises(ExpiredSignatureError):
        decode_access_token(access_token)
