from typing import List
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl

class Settings(BaseSettings):
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Toki Pona API"

    # CORS Settings
    CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000"]

    # Database Settings
    DATABASE_URL: str
    SQLALCHEMY_ECHO: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
