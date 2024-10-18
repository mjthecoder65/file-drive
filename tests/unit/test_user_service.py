import uuid

import pytest
from faker import Faker
from fastapi import HTTPException

from services.user import UserService
from tests.common import get_random_user


async def test_register_user(user_service: UserService):
    new_user = get_random_user()

    user = await user_service.register(
        username=new_user.username, email=new_user.email, password=new_user.password
    )

    assert user.username == new_user.username
    assert user.email == new_user.email


async def test_create_user_duplicate_email(user_service: UserService):
    new_user = get_random_user()
    user = await user_service.register(
        username=new_user.username, email=new_user.email, password=new_user.password
    )

    assert user.username == new_user.username
    assert user.email == new_user.email

    faker = Faker()

    with pytest.raises(HTTPException):
        await user_service.register(
            username=faker.user_name(), email=new_user.email, password=faker.password()
        )


async def test_login_user(user_service: UserService):
    new_user = get_random_user()

    user = await user_service.register(
        username=new_user.username, email=new_user.email, password=new_user.password
    )

    assert user.username == new_user.username
    assert user.email == new_user.email

    user = await user_service.login(email=new_user.email, password=new_user.password)

    assert user.username == new_user.username
    assert user.email == new_user.email


async def test_login_user_wrong_email(user_service: UserService):
    new_user = get_random_user()

    user = await user_service.register(
        username=new_user.username, email=new_user.email, password=new_user.password
    )

    assert user.username == new_user.username
    assert user.email == new_user.email

    faker = Faker()

    with pytest.raises(HTTPException):
        await user_service.login(email=faker.email(), password=new_user.password)


async def test_login_user_wrong_password(user_service: UserService):
    new_user = get_random_user()

    user = await user_service.register(
        username=new_user.username, email=new_user.email, password=new_user.password
    )

    assert user.username == new_user.username
    assert user.email == new_user.email

    faker = Faker()

    with pytest.raises(HTTPException):
        await user_service.login(email=new_user.email, password=faker.password())


async def test_get_user(user_service: UserService):
    new_user = get_random_user()

    user = await user_service.register(
        username=new_user.username, email=new_user.email, password=new_user.password
    )

    assert user.username == new_user.username
    assert user.email == new_user.email

    user = await user_service.get_by_id(user.id)

    assert user.username == new_user.username
    assert user.email == new_user.email


async def test_get_user_not_found(user_service: UserService):

    new_user = get_random_user()

    user = await user_service.register(
        username=new_user.username, email=new_user.email, password=new_user.password
    )

    assert user.username == new_user.username
    assert user.email == new_user.email

    with pytest.raises(HTTPException):
        await user_service.get_by_id(uuid.uuid4())


async def test_get_all_users(user_service: UserService):

    new_user = get_random_user()

    user = await user_service.register(
        username=new_user.username, email=new_user.email, password=new_user.password
    )

    assert user.username == new_user.username
    assert user.email == new_user.email

    users = await user_service.get_all(limit=10, offset=0)

    assert len(users) > 0
    assert users[0].username == new_user.username
    assert users[0].email == new_user.email


async def test_change_password(user_service: UserService):
    new_user = get_random_user()

    user = await user_service.register(
        username=new_user.username, email=new_user.email, password=new_user.password
    )

    assert user.username == new_user.username
    assert user.email == new_user.email

    faker = Faker()
    new_password = faker.password()
    user = await user_service.change_password(
        user=user, old_password=new_user.password, new_password=new_password
    )

    assert user.username == new_user.username
    assert user.email == new_user.email
    assert user.password_hash != new_user.password
    assert user.password_hash != new_password


async def test_change_password_wrong_password(user_service: UserService):
    new_user = get_random_user()

    user = await user_service.register(
        username=new_user.username, email=new_user.email, password=new_user.password
    )

    assert user.username == new_user.username
    assert user.email == new_user.email

    faker = Faker()
    new_password = faker.password()

    with pytest.raises(HTTPException):
        await user_service.change_password(
            user=user, old_password=faker.password(), new_password=new_password
        )
