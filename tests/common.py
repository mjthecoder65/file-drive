from pydantic import BaseModel
from faker import Faker


class UserIn(BaseModel):
    username: str
    email: str
    password: str


def get_random_user():
    faker = Faker()
    username = faker.user_name()
    email = faker.email()
    password = faker.password()

    return UserIn(username=username, email=email, password=password)
