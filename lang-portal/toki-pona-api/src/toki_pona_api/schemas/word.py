from typing import Dict
from pydantic import BaseModel, ConfigDict

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

    model_config = ConfigDict(from_attributes=True)
