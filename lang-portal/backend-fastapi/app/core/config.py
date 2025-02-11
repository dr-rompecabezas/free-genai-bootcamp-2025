from typing import List
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl

class Settings(BaseSettings):
    PROJECT_NAME: str = "Language Learning Portal"
    API_V1_STR: str = "/api/v1"
    
    # Database
    SQLITE_DATABASE_URL: str = "sqlite+aiosqlite:///./words.db"
    
    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:5173",  # Default Vite dev server
        "http://127.0.0.1:5173",
    ]
    
    class Config:
        case_sensitive = True

settings = Settings()
