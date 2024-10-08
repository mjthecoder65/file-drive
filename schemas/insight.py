from datetime import datetime

from pydantic import BaseModel, Field


class InsightGeneratePayloadModel(BaseModel):
    prompt: str = Field(..., min_length=10, max_length=1024)
    file_id: str


class InsightResponseModel(BaseModel):
    prompt: str
    response: str
    created_at: datetime
    updated_at: datetime
