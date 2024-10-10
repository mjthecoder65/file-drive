import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserResponseModel(BaseModel):
    id: uuid.UUID
    email: EmailStr
    username: str = Field(..., min_length=6, max_length=50)
    created_at: datetime
    updated_at: datetime
    last_login_at: datetime


class PaginatedUserResponseModel(BaseModel):
    users: list[UserResponseModel]
    total: int
    limit: int
    offset: int


class ChangeUserPasswordModel(BaseModel):
    old_password: str = Field(..., min_length=8, max_length=256)
    new_password: str = Field(..., min_length=8, max_length=256)
