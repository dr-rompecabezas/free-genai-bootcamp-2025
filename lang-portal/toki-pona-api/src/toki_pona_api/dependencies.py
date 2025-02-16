from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from .db.session import SessionLocal

def get_db() -> Generator:
    """
    Dependency for getting database session
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# Add more dependencies as needed, such as:
# - Authentication
# - Rate limiting
# - Caching
