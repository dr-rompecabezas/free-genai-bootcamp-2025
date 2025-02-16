from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Toki Pona API"

    # CORS Settings
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]  # Frontend URL

    # Database Settings
    SQLALCHEMY_DATABASE_URI: str
    SQLALCHEMY_ECHO: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
