from datetime import datetime
from pydantic import BaseModel, ConfigDict

class StudyActivityBase(BaseModel):
    name: str
    url: str
    description: str

class StudyActivity(StudyActivityBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class StudySessionBase(BaseModel):
    group_id: int
    study_activity_id: int

class StudySessionCreate(StudySessionBase):
    pass

class StudySession(StudySessionBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class WordReviewBase(BaseModel):
    word_id: int
    correct: bool

class WordReviewCreate(WordReviewBase):
    pass

class WordReview(WordReviewBase):
    id: int
    study_session_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
