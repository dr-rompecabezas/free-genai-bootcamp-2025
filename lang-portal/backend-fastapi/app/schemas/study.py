from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class StudySessionBase(BaseModel):
    group_id: int

class StudySessionCreate(StudySessionBase):
    pass

class StudySessionUpdate(StudySessionBase):
    completed_at: Optional[datetime] = None

class StudySession(StudySessionBase):
    id: int
    started_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class StudyActivityBase(BaseModel):
    session_id: int
    word_id: int
    correct: bool
    url: Optional[str] = None

class StudyActivityCreate(StudyActivityBase):
    pass

class StudyActivity(StudyActivityBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
