from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator

class Settings(BaseSettings):
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Toki Pona API"

    # CORS Settings
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    # Database Settings
    DATABASE_URL: str = "sqlite:///./tokipona.db"
    SQLALCHEMY_ECHO: bool = False

    # Pagination Settings
    PAGE_SIZE: int = 100

    @field_validator("CORS_ORIGINS", mode="before")
    def validate_cors_origins(cls, v):
        if isinstance(v, str):
            import json
            return json.loads(v)
        return v

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        env_file_encoding='utf-8'
    )

settings = Settings()
