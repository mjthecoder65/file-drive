from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    APP_VERSION: str = "1.0.0"
    APP_NAME: str = "File-drive Backend API"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URL: PostgresDsn
    JWT_SECRET_KEY: str
    FILE_DRIVE_UPLOADS_BUCKET_NAME: str
    GOOGLE_CLOUD_PROJECT: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
