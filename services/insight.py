import vertexai
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from vertexai.preview.generative_models import GenerativeModel, Part

from configs.settings import settings
from repositories.file import FileRepository
from repositories.insight import InsightRepository

GEMINI_MODEL_NAME = "gemini-1.5-flash-002"


class InsightService:
    def __init__(self, db: AsyncSession):
        self.insight_repo = InsightRepository(db)
        self.db = db
        self.bucket_name = settings.GCS_BUCKET_NAME
        self.file_repo = FileRepository(db)

    async def generate_insight(self, prompt, file_id: str):
        file = await self.file_repo.get_by_id(file_id)
        if not file:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
            )
        vertexai.init(project=settings.GOOGLE_CLOUD_PROJECT, location="asia-northeast3")
        model = GenerativeModel(GEMINI_MODEL_NAME)

        file = Part.from_uri(file.url, mime_type=file.mime_type)
        content = [
            prompt,
            file,
        ]

        response = model.generate_content(content)
        await self.save_insight(response.text, prompt, file.user_id, file_id)

        return response.text

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
