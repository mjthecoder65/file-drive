from pydantic import BaseModel, EmailStr, Field


class RegisterPayloadModel(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=2, max_length=50)
    password: str = Field(..., min_length=8, max_length=1024)


class LoginModel(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=1024)


class AuthTokenResponseModel(BaseModel):
    access_token: str
    token_type: str
