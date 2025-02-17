from typing import List, Optional
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, desc

from .base import CRUDBase
from ..models.group import Group
from ..models.word import Word
from ..schemas.group import GroupCreate, GroupBase
from ..api.v1.utils import SortOrder

class CRUDGroup(CRUDBase[Group, GroupCreate, GroupBase]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Group]:
        stmt = (
            select(Group)
            .where(Group.name == name)
            .options(selectinload(Group.words))
        )
        return db.execute(stmt).scalar_one_or_none()

    def add_word(self, db: Session, *, group_id: int, word_id: int) -> Group:
        group = self.get(db, id=group_id)
        stmt = select(Word).where(Word.id == word_id)
        word = db.execute(stmt).scalar_one_or_none()
        group.words.append(word)
        db.commit()
        db.refresh(group)
        return group
    
    def remove_word(self, db: Session, *, group_id: int, word_id: int) -> Group:
        """Remove a word from a group."""
        group = self.get(db, id=group_id)
        stmt = select(Word).where(Word.id == word_id)
        word = db.execute(stmt).scalar_one_or_none()
        if not word:
            raise ValueError(f"Word with id {word_id} not found")
        if word not in group.words:
            raise ValueError(f"Word with id {word_id} is not in group {group_id}")
        group.words.remove(word)
        db.commit()
        db.refresh(group)
        return group
    
    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = "name",
        order: SortOrder = SortOrder.ASC
    ) -> List[Group]:
        """Override get_multi to support sorting."""
        # Create base query
        stmt = select(self.model).options(selectinload(Group.words))
        
        # Get the column to sort by
        sort_column = getattr(self.model, sort_by)
        
        # Apply sort order
        if order == SortOrder.DESC:
            sort_column = desc(sort_column)
        
        # Apply sorting, offset, and limit
        stmt = stmt.order_by(sort_column).offset(skip).limit(limit)
        return list(db.execute(stmt).scalars().all())

crud_group = CRUDGroup(Group)
