from pydantic import BaseModel

class WordBase(BaseModel):
    word: str
    definition: str
    examples: str | None = None

class WordCreate(WordBase):
    pass

class Word(WordBase):
    id: int

    class Config:
        from_attributes = True
