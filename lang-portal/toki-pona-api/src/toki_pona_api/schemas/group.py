from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class GroupBase(BaseModel):
    name: str
    description: Optional[str] = None

class GroupCreate(GroupBase):
    pass

class Group(GroupBase):
    id: int
    words_count: int = 0

    model_config = ConfigDict(from_attributes=True)
