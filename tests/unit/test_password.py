import random

import pytest
from faker import Faker

from security.password import get_password_hash, verify_password


def test_password_raise_error():
    with pytest.raises(ValueError, match="Password must be a string or bytes"):
        password = random.randint(1, 10000)
        get_password_hash(password)

    with pytest.raises(ValueError, match="Password must be a string or bytes"):
        password = random.randint(1, 10000)
        verify_password(password, password)


def test_get_password_hash():
    faker = Faker()
    password = faker.password()
    hashed_password = get_password_hash(password)
    assert hashed_password is not None
    assert hashed_password != password
    assert verify_password(password, hashed_password)
    assert not verify_password(str(faker.password()), hashed_password)
