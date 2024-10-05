from fastapi import APIRouter
from pydantic import BaseModel, EmailStr, Field

from configs.settings import settings

router = APIRouter(prefix=f"/{settings.API_ENDPOINT_PREFIX}/auth", tags=["Auth"])


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
async def login(payload: LoginModel):
    pass
