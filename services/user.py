import pytz
from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from repositories.user import UserRepository
from security.password import get_password_hash, verify_password


class UserService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)

    async def register(self, username: str, email: str, password: str) -> User:
        user = await self.user_repo.get_by_email(email)

        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists",
            )

        new_user = User(
            email=email, username=username, password_hash=get_password_hash(password)
        )

        return await self.user_repo.add(new_user)

    async def login(self, email: str, password: str) -> User:
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Wrong email or password",
            )
        if not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Wrong email or password"
            )
        user.last_login_at = datetime.now(pytz.utc)
        return user

    async def get_by_id(self, user_id: str) -> User:
        user = await self.user_repo.get_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user
