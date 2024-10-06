from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.file import File


class FileRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.model = File

    async def add(self, file: File) -> File:
        self.db.add(file)
        await self.db.commit()
        await self.db.refresh(file)
        return file

    async def get_by_user_id(self, user_id: str) -> list[File]:
        result = await self.db.execute(
            select(self.model)
            .filter_by(user_id=user_id)
            .order_by(self.model.created_at.desc())
        )
        return result.scalars().all()

    async def get_by_name(self, name: str) -> File:
        result = await self.db.execute(select(self.model).filter_by(name=name))
        return result.scalars().first()

    async def get_by_id(self, id: str) -> File:
        result = await self.db.execute(select(self.model).filter_by(id=id))
        return result.scalars().first()

    async def get_all(self) -> list[File]:
        result = await self.db.execute(select(self.model))
        return result.scalars().all()

    async def delete(self, file: File):
        self.db.delete(file)
        await self.db.commit()
