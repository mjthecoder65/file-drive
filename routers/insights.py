import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import get_current_user
from configs.database import get_session
from configs.settings import settings
from models.user import User
from services.insight import InsightService

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
    _: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    insight_service = InsightService(db)
    return await insight_service.generate_insight(
        prompt=payload.prompt, file_id=payload.file_id
    )


@router.get("/{id}")
async def get_insight(
    id: uuid.UUID,
    _: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    insight_service = InsightService(db)
    return await insight_service.get_insight_by_id(insight_id=id)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_insights(
    file_id: uuid.UUID,
    _: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    insight_service = InsightService(db)
    return await insight_service.delete_insight_by_id(insight_id=file_id)
