import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import get_current_user, only_admin_user
from configs.database import get_session
from configs.settings import settings
from models.user import User
from services.file import FileService
from services.user import UserService

router = APIRouter(prefix=f"{settings.API_ENDPOINT_PREFIX}/users", tags=["Users"])


class UserResponseModel(BaseModel):
    id: uuid.UUID
    email: EmailStr
    username: str = Field(..., min_length=6, max_length=50)
    created_at: datetime
    updated_at: datetime
    last_login_at: datetime


@router.get(
    "",
    dependencies=[Depends(only_admin_user)],
    status_code=status.HTTP_200_OK,
    response_model=list[UserResponseModel],
)
async def get_all_users(db: Annotated[AsyncSession, Depends(get_session)]):
    # TODO: Implement pagination.
    user_service = UserService(db)
    return await user_service.get_all()


@router.get(
    "/me",
    dependencies=[Depends(only_admin_user)],
    status_code=status.HTTP_200_OK,
    response_model=UserResponseModel,
)
async def get_logged_in_user(user: Annotated[User, Depends(get_current_user)]):
    return user


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserResponseModel)
async def get_user_by_id(
    id: uuid.UUID, db: Annotated[AsyncSession, Depends(get_session)]
):
    user_service = UserService(db)
    return await user_service.get_by_id(id)


@router.get("/{id}/files", status_code=status.HTTP_200_OK)
async def get_user_files(
    id: uuid.UUID,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    # TODO: Implement pagination.
    if user.id != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    file_service = FileService(db)
    return await file_service.get_files_by_user_id(user.id)


class ChangeUserPasswordModel(BaseModel):
    old_password: str = Field(..., min_length=8, max_length=1024)
    new_password: str = Field(..., min_length=8, max_length=1024)


@router.put(
    "/{id}/change-password",
    status_code=status.HTTP_200_OK,
    response_model=UserResponseModel,
)
async def change_user_password(
    id: uuid.UUID,
    payload: ChangeUserPasswordModel,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    if user.id != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    user_service = UserService(db)

    return await user_service.change_password(
        user=user, old_password=payload.old_password, new_password=payload.new_password
    )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_account(
    id: uuid.UUID,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    if user.id != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    user_service = UserService(db)
    await user_service.delete(user.id)
