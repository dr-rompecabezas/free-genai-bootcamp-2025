from pydantic import BaseModel
from typing import Optional

class WordBase(BaseModel):
    kanji: str
    romaji: str
    english: str
    parts: str  # JSON string
    group_id: Optional[int] = None

class WordCreate(WordBase):
    pass

class WordUpdate(BaseModel):
    kanji: Optional[str] = None
    romaji: Optional[str] = None
    english: Optional[str] = None
    parts: Optional[str] = None
    group_id: Optional[int] = None

class Word(WordBase):
    id: int

    class Config:
        from_attributes = True
