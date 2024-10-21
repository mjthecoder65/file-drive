from pydantic import BaseModel, Field


class PaginationBaseModel(BaseModel):
    limit: int = Field(10, ge=1)
    offset: int = Field(0, ge=0)
    total: int = Field(..., ge=0)
