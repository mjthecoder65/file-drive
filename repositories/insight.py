from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.insight import Insight


class InsightRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.model = Insight

    async def get_insights_by_file_id(self, file_id: str):
        result = await self.db.execute(select(self.model).filter_by(file_id=file_id))
        return result.all()

    async def add(
        self, insight_data: str, prompt: str, user_id: str, file_id: str
    ) -> Insight:
        new_insight = self.model(
            insight_data=insight_data, prompt=prompt, file_id=file_id, user_id=user_id
        )
        await self.db.add(new_insight)
        await self.db.commit()
        await self.db.refresh(new_insight)
        return new_insight
