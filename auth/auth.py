import uuid
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from configs.database import get_session
from configs.settings import settings
from models.user import User
from services.user import UserService


def create_access_token(id: uuid.UUID, is_admin: bool = False) -> str:
    return jwt.encode(
        claims={
            "sub": str(id),
            "is_admin": is_admin,
            "exp": datetime.now()
            + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES),
        },
        key=settings.JWT_SECRET_KEY,
    )


async def get_current_user(
    token: str = Depends(
        OAuth2PasswordBearer(tokenUrl=f"{settings.API_ENDPOINT_PREFIX}/auth/login")
    ),
    db: AsyncSession = Depends(get_session),
) -> User:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY)
        user_id: str = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

        user_service = UserService(db)
        user = await user_service.get_by_id(user_id)
        return user
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication Token has expired",
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


async def only_admin_user(user: User = Depends(get_current_user)) -> bool:
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource.s",
        )
    return True
