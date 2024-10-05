from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, status
from pydantic import BaseModel

from auth.auth import get_current_user
from configs.settings import settings
from models.user import User

router = APIRouter(prefix=f"{settings.API_ENDPOINT_PREFIX}/files", tags=["Files"])


class FileResponseModel(BaseModel):
    name: str
    url: str
    created_at: datetime
    updated_at: datetime


@router.post("", status_code=status.HTTP_200_OK, response_model=FileResponseModel)
async def upload_file(
    file: UploadFile, user: Annotated[User, Depends(get_current_user)]
):
    pass


@router.get("", response_model=list[FileResponseModel])
async def get_all_files(user: Annotated[User, Depends(get_current_user)]):
    """Get all files uploaded users."""
    pass


@router.get("/{id}", response_model=FileResponseModel)
async def get_file_by_id(id: str, user: Annotated[User, Depends(get_current_user)]):
    pass


@router.get("/{id}/insights", response_model=FileResponseModel)
async def get_file_by_id(id: str, user: Annotated[User, Depends(get_current_user)]):
    pass


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(id: str, user: Annotated[User, Depends(get_current_user)]):
    pass
