import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import get_current_user, only_admin_user
from configs.database import get_session
from configs.settings import settings
from models import file
from models.user import User
from schemas.file import PaginatedFileResponseModel
from schemas.user import (
    ChangeUserPasswordModel,
    PaginatedUserResponseModel,
    UserResponseModel,
)
from services.file import FileService
from services.user import UserService

router = APIRouter(prefix=f"{settings.API_ENDPOINT_PREFIX}/users", tags=["Users"])


@router.get(
    "",
    dependencies=[Depends(only_admin_user)],
    status_code=status.HTTP_200_OK,
    response_model=PaginatedUserResponseModel,
)
async def get_all_users(
    db: Annotated[AsyncSession, Depends(get_session)],
    limit: int = Query(default=10, ge=1, le=50),
    offset: int = Query(default=0, ge=0),
):
    user_service = UserService(db)
    count = await user_service.get_count()
    users = await user_service.get_all(limit=limit, offset=offset)

    return {
        "data": users,
        "total": count,
        "limit": limit,
        "offset": offset,
    }


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=UserResponseModel,
)
async def get_current_in_user(user: Annotated[User, Depends(get_current_user)]):
    return user


@router.get(
    "/{id}",
    dependencies=[Depends(only_admin_user)],
    status_code=status.HTTP_200_OK,
    response_model=UserResponseModel,
)
async def get_user_by_id(
    id: uuid.UUID, db: Annotated[AsyncSession, Depends(get_session)]
):
    user_service = UserService(db)
    return await user_service.get_by_id(id)


@router.get(
    "/{id}/files",
    status_code=status.HTTP_200_OK,
    response_model=PaginatedFileResponseModel,
)
async def get_user_files(
    id: uuid.UUID,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
    limit: int = Query(default=10, ge=1, le=20),
    offset: int = Query(default=0, ge=0),
):
    if user.id != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    file_service = FileService(db)
    files = await file_service.get_files_by_user_id(user.id, limit=limit, offset=offset)
    count = await file_service.get_files_count_by_user_id(user.id)

    return {
        "data": files,
        "total": count,
        "limit": limit,
        "offset": offset,
    }


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
    await user_service.delete_user_by_id(user.id)
