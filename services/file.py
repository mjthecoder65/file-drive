import uuid

from fastapi import HTTPException, UploadFile, status
from google.cloud import storage
from sqlalchemy.ext.asyncio import AsyncSession

from configs.settings import settings
from models.file import File
from repositories.file import FileRepository


class FileService:
    def __init__(self, db: AsyncSession):
        self.file_repo = FileRepository(db)
        self.db = db
        self.bucket_name = settings.GCS_BUCKET_NAME

    def _upload_to_gcs(self, file_name: str, file: UploadFile):
        client = storage.Client()
        bucket = client.bucket(bucket_name=self.bucket_name)
        blob = bucket.blob(file_name)
        blob.upload_from_file(file.file)

    async def upload_file(self, user_id: str, file_name: str, file: UploadFile) -> File:
        file_id = str(uuid.uuid4())
        self._upload_to_gcs(file_name, file)
        new_file = File(file_id=file_id, name=file_name, user_id=user_id)
        return await self.file_repo.add(new_file)

    async def get_files_by_user_id(self, user_id: str) -> list[File]:
        file = await self.file_repo.get_by_user_id(user_id)
        if not file:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
            )

    async def delete_file_by_id(self, file_id: str):
        file = await self.file_repo.get_by_id(file_id)

        if not file:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
            )

        client = storage.Client()
        bucket = client.bucket(bucket_name=self.bucket_name)
        blob = bucket.blob(file.name)
        blob.delete()
        return await self.file_repo.delete(id=file.id)
