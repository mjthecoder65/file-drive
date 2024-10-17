from datetime import datetime

import pytz
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
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Wrong email or password",
            )
        if not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Wrong email or password",
            )
        user.last_login_at = datetime.now(pytz.utc)
        return await self.user_repo.update(user)

    async def get_by_id(self, user_id: str) -> User:
        user = await self.user_repo.get_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user

    async def get_all(self, limit: int, offset: int) -> list[User]:
        return await self.user_repo.get_all(limit=limit, offset=offset)

    async def get_count(self) -> int:
        return await self.user_repo.get_count()

    async def change_password(
        self, user: User, old_password: str, new_password: str
    ) -> User:
        if not verify_password(old_password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Old password is incorrect",
            )

        user.password_hash = get_password_hash(new_password)
        return await self.user_repo.update(user)
