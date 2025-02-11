from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class WordBase(BaseModel):
    word: str
    reading: str
    meaning: str
    group_id: int

class WordCreate(WordBase):
    pass

class WordUpdate(BaseModel):
    word: Optional[str] = None
    reading: Optional[str] = None
    meaning: Optional[str] = None
    group_id: Optional[int] = None

class Word(WordBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
