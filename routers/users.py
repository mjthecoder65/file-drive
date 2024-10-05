from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, status, Depends
from pydantic import BaseModel, EmailStr, Field
from auth.auth import get_current_user
from models.user import User

router = APIRouter(prefix="/users", tags=["Users"])


class UserResponseModel(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=6, max_length=50)
    created_at: datetime
    updated_at: datetime


@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserResponseModel)
async def get_logged_in_user(user: Annotated[User, Depends(get_current_user)]):
    pass


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserResponseModel)
async def get_user_by_id(id: str, user: Annotated[User, Depends(get_current_user)]):
    pass


@router.get("/{id}/files", status_code=status.HTTP_200_OK)
async def get_user_files(id: str, user: Annotated[User, Depends(get_current_user)]):
    pass


@router.put(
    "/{id}/change-password",
    status_code=status.HTTP_200_OK,
    response_model=UserResponseModel,
)
async def change_user_password(
    id: str, user: Annotated[User, Depends(get_current_user)]
):
    pass


class ChangeUserPasswordModel(BaseModel):
    old_password: str = Field(..., min_length=8, max_length=1024)
    new_password: str = Field(..., min_length=8, max_length=1024)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_account(
    payload: ChangeUserPasswordModel,
    id: str,
    user: Annotated[User, Depends(get_current_user)],
):
    pass
