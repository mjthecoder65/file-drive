import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, HttpUrl


class FileResponseModel(BaseModel):
    id: uuid.UUID
    name: str
    extension: str
    mime_type: str
    url: HttpUrl
    size: Decimal
    created_at: datetime
    updated_at: datetime


class PaginatedFileResponseModel(BaseModel):
    files: list[FileResponseModel]
    total: int
    limit: int
    offset: int
