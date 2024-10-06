from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_VERSION: str = "v1"
    API_ENDPOINT_PREFIX: str = "/api/v1"
    APP_ENV: str = "development"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8080
    APP_NAME: str = "FileDrive API"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URL: PostgresDsn
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 2
    GCS_BUCKET_NAME: str
    GOOGLE_CLOUD_PROJECT: str
    GEMINI_API_KEY: str
    GEMINI_MODEL_NAME: str = "gemini-pro-vision"
    LOCATION: str = "asia-northeast3"

    @property
    def debug(self) -> bool:
        return self.APP_ENV == "development"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
