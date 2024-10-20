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

    async def get_all(self, limit: int, offset: int) -> list[User]:
        result = await self.db.execute(select(self.model).limit(limit).offset(offset))
        return result.scalars().all()

    async def add(self, user: User) -> User:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update(self, user: User) -> User:
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_count(self) -> int:
        result = await self.db.execute(select(self.model))
        return len(result.scalars().all())

    async def delete(self, user: User):
        self.db.delete(user)
        await self.db.commit()
        return user
