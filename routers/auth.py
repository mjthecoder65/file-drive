from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import create_access_token
from configs.database import get_session
from configs.settings import settings
from schemas.auth import AuthTokenResponseModel, RegisterPayloadModel
from services.user import UserService

router = APIRouter(prefix=f"{settings.API_ENDPOINT_PREFIX}/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=AuthTokenResponseModel,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    payload: RegisterPayloadModel, db: Annotated[AsyncSession, Depends(get_session)]
):
    user_service = UserService(db)
    user = await user_service.register(
        username=payload.username, email=payload.email, password=payload.password
    )

    return {
        "access_token": create_access_token(
            id=user.id,
            is_admin=user.is_admin,
            expires_datetime=datetime.now(tz=timezone.utc) + timedelta(hours=2),
        ),
        "token_type": "bearer",
    }


@router.post("/login", response_model=AuthTokenResponseModel)
async def login(
    db: Annotated[AsyncSession, Depends(get_session)],
    form: OAuth2PasswordRequestForm = Depends(),
):
    user_service = UserService(db)
    user = await user_service.login(email=form.username, password=form.password)

    return {
        "access_token": create_access_token(
            id=user.id,
            is_admin=user.is_admin,
            expires_datetime=datetime.now(tz=timezone.utc) + timedelta(hours=2),
        ),
        "token_type": "bearer",
    }
