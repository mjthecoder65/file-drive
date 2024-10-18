import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from schemas.pagination import PaginationBaseModel


class UserResponseModel(BaseModel):
    id: uuid.UUID
    email: EmailStr
    username: str = Field(..., min_length=6, max_length=50)
    created_at: datetime
    updated_at: datetime
    last_login_at: datetime | None = None

    class Config:
        from_attribues = True


class PaginatedUserResponseModel(PaginationBaseModel):
    data: list[UserResponseModel]


class ChangeUserPasswordModel(BaseModel):
    old_password: str = Field(..., min_length=8, max_length=256)
    new_password: str = Field(..., min_length=8, max_length=256)
