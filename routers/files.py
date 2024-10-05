from datetime import datetime

from fastapi import APIRouter, Path, UploadFile, status
from pydantic import BaseModel

from configs.settings import settings

router = APIRouter(prefix=f"{settings.API_ENDPOINT_PREFIX}/files", tags=["Files"])


class FileResponseModel(BaseModel):
    name: str
    url: str
    created_at: datetime
    updated_at: datetime


@router.post("", status_code=status.HTTP_200_OK, response_model=FileResponseModel)
async def upload_file(file: UploadFile):
    pass


@router.get("", response_model=list[FileResponseModel])
async def get_all_files():
    """Get all files uploaded users."""
    pass


@router.get("/{id}", response_model=FileResponseModel)
async def get_file_by_id(id: str = Path(...)):
    pass


@router.get("/{id}/insights", response_model=FileResponseModel)
async def get_file_by_id(id: str = Path(...)):
    pass


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(id: str = Path(...)):
    pass
