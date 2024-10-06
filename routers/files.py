import uuid
from datetime import datetime
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, status
from pydantic import BaseModel, HttpUrl
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import get_current_user, only_admin_user
from configs.database import get_session
from configs.settings import settings
from models import insight
from models.user import User
from services.file import FileService
from services.insight import InsightService

router = APIRouter(prefix=f"{settings.API_ENDPOINT_PREFIX}/files", tags=["Files"])


class FileResponseModel(BaseModel):
    id: uuid.UUID
    name: str
    extension: str
    mime_type: str
    url: HttpUrl  # Signed URL
    size: Decimal
    created_at: datetime
    updated_at: datetime


@router.post("", status_code=status.HTTP_200_OK, response_model=FileResponseModel)
async def upload_file(
    file: UploadFile,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    file_service = FileService(db)
    return await file_service.upload_file(user_id=user.id, file=file)


@router.get(
    "", dependencies=[Depends(only_admin_user)], response_model=list[FileResponseModel]
)
async def get_all_files(db: Annotated[AsyncSession, Depends(get_session)]):
    file_service = FileService(db)
    return await file_service.get_all_files()


@router.get(
    "/{id}", dependencies=[Depends(only_admin_user)], response_model=FileResponseModel
)
async def get_file_by_id(
    id: uuid.UUID, db: Annotated[AsyncSession, Depends(get_session)]
):
    file_service = FileService(db)
    return await file_service.get_file_by_id(id)


@router.get("/{id}/insights")
async def get_file_by_id(
    id: uuid.UUID,
    _: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    insight_service = InsightService(db)
    return await insight_service.get_insights_by_file_id(file_id=id)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(
    id: uuid.UUID,
    _: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    file_service = FileService(db)
    await file_service.delete_file_by_id(file_id=id)
    return None
