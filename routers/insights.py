from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from auth.auth import get_current_user
from configs.settings import settings
from models.user import User

router = APIRouter(prefix=f"{settings.API_ENDPOINT_PREFIX}/insights", tags=["Insights"])


class InsightGeneratePayloadModel(BaseModel):
    prompt: str = Field(..., min_length=10, max_length=1024)
    file_id: str


class InsightResponseModel(BaseModel):
    prompt: str
    response: str
    created_at: datetime
    updated_at: datetime


@router.post("")
async def generate_insights(
    payload: InsightGeneratePayloadModel,
    user: Annotated[User, Depends(get_current_user)],
):
    raise NotImplementedError("This feature is not implemented yet.")


@router.get("/{id}", response_model=list[InsightResponseModel])
async def get_insights(id: str, user: Annotated[User, Depends(get_current_user)]):
    raise NotImplementedError("This feature is not implemented yet.")


@router.get("/{id}/download", response_model=list[InsightResponseModel])
async def download_insight(id: str, user: Annotated[User, Depends(get_current_user)]):
    """Allows you to download insight as a file. PDF, DOCX, TXT, etc."""
    raise NotImplementedError("This feature is not implemented yet.")


@router.delete("/{id}")
async def delete_insights(
    file_id: str, user: Annotated[User, Depends(get_current_user)]
):
    raise NotImplementedError("This feature is not implemented yet.")
