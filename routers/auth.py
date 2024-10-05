from fastapi import APIRouter, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field

from configs.settings import settings
from sqlalchemy.ext.asyncio import AsyncSession
from configs.database import get_session

router = APIRouter(prefix=f"{settings.API_ENDPOINT_PREFIX}/auth", tags=["Auth"])


class RegisterPayloadModel(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=6, max_length=50)
    password: str = Field(..., min_length=8, max_length=1024)


class LoginModel(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=1024)


@router.post("/register")
async def register_user(payload: RegisterPayloadModel):
    pass


@router.post("/login")
async def login(
    db: Annotated[AsyncSession, Depends(get_session)],
    form: OAuth2PasswordRequestForm = Depends(),
):
    pass
