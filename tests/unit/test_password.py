from security.password import get_password_hash, verify_password
from faker import Faker


def test_get_password_hash():
    faker = Faker()
    password = faker.password()
    hashed_password = get_password_hash(password)
    assert hashed_password is not None
    assert hashed_password != password
    assert verify_password(password, hashed_password)


def test_verify_password():
    faker = Faker()
    password = faker.password()
    hashed_password = get_password_hash(password)
    assert verify_password(password, hashed_password)
    assert not verify_password(faker.password(), hashed_password)
    assert not verify_password(password, get_password_hash(faker.password()))
    assert not verify_password(faker.password(), get_password_hash(faker.password()))
