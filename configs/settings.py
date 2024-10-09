from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_VERSION: str = "v1"
    API_ENDPOINT_PREFIX: str = "/api/v1"
    APP_ENV: str = "development"
    APP_NAME: str = "FileDrive API"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 2
    JWT_SECRET_KEY: str
    DATABASE_URL: str
    DATABASE_URL_TEST: str = "sqlite+aiosqlite:///./test.db"
    GCS_BUCKET_NAME: str
    GOOGLE_CLOUD_PROJECT: str
    GEMINI_MODEL_NAME: str = "gemini-pro-vision"
    GOOGLE_CLOUD_REGION: str

    @property
    def debug(self) -> bool:
        return self.APP_ENV == "development"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
