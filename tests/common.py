from random import randint

from faker import Faker

from schemas.user import UserIn


def get_random_user():
    faker = Faker()
    username = faker.user_name()
    email = faker.email()
    password = faker.password(length=randint(8, 256))

    return UserIn(username=username, email=email, password=password)
