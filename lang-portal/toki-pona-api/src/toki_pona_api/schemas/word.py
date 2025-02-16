from typing import Dict, List
from pydantic import BaseModel

class WordBase(BaseModel):
    toki_pona: str
    english: str
    definition: str
    components: Dict[str, str] = {}

class WordCreate(WordBase):
    pass

class Word(WordBase):
    id: int
    correct_count: int = 0
    wrong_count: int = 0

    class Config:
        from_attributes = True
