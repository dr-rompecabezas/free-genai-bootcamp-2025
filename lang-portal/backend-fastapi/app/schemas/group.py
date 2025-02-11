from typing import Optional
from pydantic import BaseModel
from datetime import datetime

# Shared properties
class GroupBase(BaseModel):
    name: str
    description: Optional[str] = None
    words_count: Optional[int] = 0

# Properties to receive on item creation
class GroupCreate(GroupBase):
    pass

# Properties to receive on item update
class GroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    words_count: Optional[int] = None

# Properties shared by models stored in DB
class GroupInDBBase(GroupBase):
    id: int

    class Config:
        from_attributes = True

# Properties to return to client
class Group(GroupInDBBase):
    created_at: datetime

# Properties stored in DB
class GroupInDB(GroupInDBBase):
    created_at: datetime
