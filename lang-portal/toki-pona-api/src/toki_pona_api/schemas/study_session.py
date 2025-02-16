from datetime import datetime
from typing import List
from pydantic import BaseModel

class StudyActivityBase(BaseModel):
    name: str
    url: str
    description: str

class StudyActivity(StudyActivityBase):
    id: int

    class Config:
        from_attributes = True

class StudySessionBase(BaseModel):
    group_id: int
    study_activity_id: int

class StudySessionCreate(StudySessionBase):
    pass

class StudySession(StudySessionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class WordReviewBase(BaseModel):
    word_id: int
    correct: bool

class WordReviewCreate(WordReviewBase):
    pass

class WordReview(WordReviewBase):
    id: int
    study_session_id: int
    created_at: datetime

    class Config:
        from_attributes = True
