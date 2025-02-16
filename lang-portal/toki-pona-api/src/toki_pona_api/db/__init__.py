from datetime import datetime
from typing import List, Optional, Dict, Generator
from pydantic import BaseModel, Field
from fastapi import FastAPI, Query, HTTPException, Depends
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON, Table, create_engine
from sqlalchemy.orm import Session, relationship, DeclarativeBase, sessionmaker
from sqlalchemy.sql import func
from enum import Enum
import os
from contextlib import contextmanager

# --- Database Configuration ---

SQLITE_URL = os.getenv("DATABASE_URL", "sqlite:///./toki_pona.db")

# Create engine with proper settings for SQLite
engine = create_engine(
    SQLITE_URL,
    # Enable foreign key support in SQLite
    connect_args={"check_same_thread": False},
    # Echo SQL statements in development
    echo=os.getenv("DEBUG", "false").lower() == "true"
)

# Create session factory
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

# --- Database Session Management ---

@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """
    Context manager for database sessions.
    Ensures proper handling of sessions including error cases.
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()

def get_db() -> Generator[Session, None, None]:
    """
    Dependency for FastAPI endpoints to get database sessions.
    """
    with get_db_session() as session:
        yield session

# --- Database Initialization ---

def init_db() -> None:
    """
    Initialize the database, creating all tables.
    """
    Base.metadata.create_all(bind=engine)

def init_study_activities() -> None:
    """
    Initialize default study activities if they don't exist.
    """
    default_activities = [
        {
            "name": "Flashcards",
            "url": "/apps/flashcards",
            "description": "Practice Toki Pona words with flashcards"
        },
        {
            "name": "Quiz",
            "url": "/apps/quiz",
            "description": "Test your Toki Pona knowledge"
        },
        {
            "name": "Sentence Builder",
            "url": "/apps/sentences",
            "description": "Practice building Toki Pona sentences"
        }
    ]

    with get_db_session() as db:
        for activity in default_activities:
            existing = db.query(StudyActivityModel).filter_by(name=activity["name"]).first()
            if not existing:
                db.add(StudyActivityModel(**activity))

# --- Base Class ---

class Base(DeclarativeBase):
    pass

# [Previous SQLAlchemy Models remain the same]

# [Previous Pydantic Models remain the same]

# --- FastAPI App ---

app = FastAPI(
    title="Toki Pona Learning Portal API",
    description="A learning portal for Toki Pona language study",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    """
    Initialize database and default data on application startup.
    """
    init_db()
    init_study_activities()

# --- Error Handling ---

class DatabaseError(Exception):
    """Base exception for database operations"""
    pass

class NotFoundError(DatabaseError):
    """Raised when a requested resource is not found"""
    pass

@app.exception_handler(DatabaseError)
async def database_exception_handler(request, exc):
    """Handle database-related exceptions"""
    if isinstance(exc, NotFoundError):
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)}
        )
    return JSONResponse(
        status_code=500,
        content={"detail": "Database error occurred"}
    )



from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()