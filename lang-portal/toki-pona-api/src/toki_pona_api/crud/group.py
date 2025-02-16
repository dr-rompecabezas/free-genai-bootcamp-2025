from typing import List, Optional
from sqlalchemy.orm import Session

from .base import CRUDBase
from ..models.group import Group
from ..schemas.group import GroupCreate, GroupBase

class CRUDGroup(CRUDBase[Group, GroupCreate, GroupBase]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Group]:
        return db.query(Group).filter(Group.name == name).first()

    def add_word(self, db: Session, *, group_id: int, word_id: int) -> Group:
        group = self.get(db, id=group_id)
        word = db.query(self.model).filter(self.model.id == word_id).first()
        group.words.append(word)
        db.commit()
        db.refresh(group)
        return group

crud_group = CRUDGroup(Group)
