from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import create_access_token
from configs.database import get_session
from configs.settings import settings
from services.user import UserService

router = APIRouter(prefix=f"{settings.API_ENDPOINT_PREFIX}/auth", tags=["Auth"])


class RegisterPayloadModel(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=6, max_length=50)
    password: str = Field(..., min_length=8, max_length=1024)


class LoginModel(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=1024)


@router.post("/register")
async def register_user(
    payload: RegisterPayloadModel, db: Annotated[AsyncSession, Depends(get_session)]
):
    user_service = UserService(db)
    user = await user_service.register(
        username=payload.username, email=payload.email, password=payload.password
    )

    return {
        "access_token": create_access_token(user.id, user.is_admin),
        "token_type": "bearer",
    }


@router.post("/login")
async def login(
    db: Annotated[AsyncSession, Depends(get_session)],
    form: OAuth2PasswordRequestForm = Depends(),
):
    user_service = UserService(db)
    user = await user_service.login(email=form.username, password=form.password)

    return {
        "access_token": create_access_token(user.id, user.is_admin),
        "token_type": "bearer",
    }
