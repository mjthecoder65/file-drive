import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from configs.settings import settings
from repositories.file import FileRepository
from repositories.insight import InsightRepository
from services.gemini import GeminiService


class InsightService:
    def __init__(self, db: AsyncSession):
        self.insight_repo = InsightRepository(db)
        self.db = db
        self.bucket_name = settings.GCS_BUCKET_NAME
        self.file_repo = FileRepository(db)
        self.gemini_service = GeminiService()

    async def generate_insight(self, prompt, file_id: str):
        file = await self.file_repo.get_by_id(file_id)
        if not file:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
            )
        result = self.gemini_service.get_gemini_response(prompt, file)

        await self.insight_repo.add(
            insight_data=result,
            prompt=prompt,
            user_id=file.user_id,
            file_id=file_id,
        )

        return result

    async def save_insight(
        self, insight_data: str, prompt: str, user_id: str, file_id: str
    ):
        file = await self.file_repo.get_by_id(file_id)

        if not file:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
            )
        new_insight = await self.insight_repo.add(
            insight_data=insight_data, prompt=prompt, user_id=user_id, file_id=file_id
        )
        return new_insight

    async def get_insights_by_file_id(self, file_id: str):
        insights = await self.insight_repo.get_insights_by_file_id(file_id)
        if not insights:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Insights not found"
            )
        return insights

    async def get_insight_by_id(self, insight_id: uuid.UUID):
        insight = await self.insight_repo.get_by_id(insight_id)
        if not insight:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Insight not found"
            )
        return insight

    async def delete_insight_by_id(self, insight_id: uuid.UUID):
        insight = await self.insight_repo.get_by_id(insight_id)
        if not insight:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Insight not found"
            )
        await self.insight_repo.delete(insight)
