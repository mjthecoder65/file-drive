from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.model = User

    async def get_by_email(self, email) -> User:
        result = await self.db.execute(select(self.model).filter_by(email=email))
        return result.scalars().first()

    async def get_by_id(self, id: str | int) -> User:
        result = await self.db.execute(select(self.model).filter_by(id=id))
        return result.scalars().first()

    async def add(self, user: User) -> User:
        self.db.add(user)
        await self.db.commit()
        return user
