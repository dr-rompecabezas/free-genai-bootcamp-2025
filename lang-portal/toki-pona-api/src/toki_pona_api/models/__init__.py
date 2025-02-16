from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from fastapi import FastAPI, Query, HTTPException
from sqlalchemy.orm import Session
from enum import Enum

# --- Pydantic Models ---

class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"

class WordBase(BaseModel):
    toki_pona: str = Field(..., description="The word in Toki Pona")
    english: str = Field(..., description="English translation of the word")
    definition: str = Field(..., description="Detailed definition in English")

class Word(WordBase):
    id: int
    correct_count: int = Field(default=0)
    wrong_count: int = Field(default=0)

    class Config:
        from_attributes = True

class GroupBase(BaseModel):
    name: str = Field(..., description="Name of the word group")
    description: Optional[str] = None

class Group(GroupBase):
    id: int
    words_count: int = Field(default=0)

    class Config:
        from_attributes = True

class StudyActivityBase(BaseModel):
    name: str = Field(..., description="Name of the study activity")
    url: str = Field(..., description="URL of the study activity")
    description: Optional[str] = None

class StudyActivity(StudyActivityBase):
    id: int

    class Config:
        from_attributes = True

class StudySessionCreate(BaseModel):
    group_id: int
    study_activity_id: int

class StudySession(StudySessionCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class WordReviewCreate(BaseModel):
    word_id: int
    correct: bool

class WordReview(WordReviewCreate):
    id: int
    study_session_id: int
    created_at: datetime

    class Config:
        from_attributes = True
