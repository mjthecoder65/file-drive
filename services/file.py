from datetime import timedelta

from fastapi import HTTPException, UploadFile, status
from google.cloud import storage
from sqlalchemy.ext.asyncio import AsyncSession

from configs.settings import settings
from models.file import File
from repositories.file import FileRepository


class FileService:
    def __init__(self, db: AsyncSession):
        self.file_repo = FileRepository(db)

    def _upload_to_gcs(self, file_name: str, file: UploadFile):
        client = storage.Client()
        bucket = client.bucket(bucket_name=settings.GCS_BUCKET_NAME)
        blob = bucket.blob(file_name)
        blob.upload_from_file(file.file, content_type=file.content_type)

    def _generate_signed_url(
        self, file_name: str, expiration: int = 2 * 60 * 60
    ) -> str:
        client = storage.Client()
        bucket = client.bucket(bucket_name=settings.GCS_BUCKET_NAME)
        blob = bucket.blob(file_name)
        expiration = timedelta(seconds=expiration)
        return blob.generate_signed_url(
            expiration=expiration, response_disposition="inline"
        )

    async def upload_file(self, user_id: str, file: UploadFile) -> File:
        file_name = f"{user_id}-{file.filename}"
        self._upload_to_gcs(file_name=file_name, file=file)

        file.file.seek(0)
        content = await file.read()
        file_size = len(content)
        extension = file.filename.split(".")[-1]
        mime_type = file.content_type

        new_file = File(
            name=file_name,
            user_id=user_id,
            extension=extension,
            mime_type=mime_type,
            size=file_size,
        )

        url = self._generate_signed_url(file_name)
        result = await self.file_repo.add(new_file)

        return {
            "id": result.id,
            "name": result.name,
            "extension": result.extension,
            "mime_type": result.mime_type,
            "size": result.size,
            "url": url,
            "created_at": result.created_at,
            "updated_at": result.updated_at,
        }

    async def get_files_by_user_id(
        self, user_id: str, limit: int, offset: int
    ) -> list[File]:
        files = await self.file_repo.get_by_user_id(user_id, limit=limit, offset=offset)
        result = []

        for file in files:
            url = self._generate_signed_url(file.name)
            result.append(
                {
                    "id": file.id,
                    "name": file.name,
                    "extension": file.extension,
                    "mime_type": file.mime_type,
                    "size": file.size,
                    "url": url,
                    "created_at": file.created_at,
                    "updated_at": file.updated_at,
                }
            )
        return result

    async def get_files_count_by_user_id(self, user_id: str) -> int:
        return await self.file_repo.get_file_count(user_id=user_id)

    async def get_all_files(self, limit: int, offset: int) -> list[File]:
        files = await self.file_repo.get_all(limit=limit, offset=offset)
        result = []

        for file in files:
            url = self._generate_signed_url(file.name)
            result.append(
                {
                    "id": file.id,
                    "name": file.name,
                    "extension": file.extension,
                    "mime_type": file.mime_type,
                    "size": file.size,
                    "url": url,
                    "created_at": file.created_at,
                    "updated_at": file.updated_at,
                }
            )
        return result

    async def get_files_count(self) -> int:
        return await self.file_repo.get_file_count()

    def _delete_from_gcs(self, file_name: str):
        client = storage.Client()
        bucket = client.bucket(bucket_name=settings.GCS_BUCKET_NAME)
        blob = bucket.blob(file_name)
        blob.delete()

    async def delete_file_by_id(self, file_id: str):
        file = await self.file_repo.get_by_id(file_id)

        if not file:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
            )
        self._delete_from_gcs(file.name)

        await self.file_repo.delete(file=file)

    async def get_file_by_id(self, file_id: str) -> File:
        file = await self.file_repo.get_by_id(file_id)
        if not file:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
            )
        url = self._generate_signed_url(file.name)
        return {
            "id": file.id,
            "name": file.name,
            "extension": file.extension,
            "mime_type": file.mime_type,
            "size": file.size,
            "url": url,
            "created_at": file.created_at,
            "updated_at": file.updated_at,
        }
