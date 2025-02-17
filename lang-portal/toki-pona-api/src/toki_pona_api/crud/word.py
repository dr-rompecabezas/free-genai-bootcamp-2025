from typing import List, Optional
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, desc

from .base import CRUDBase
from ..models.word import Word
from ..schemas.word import WordCreate, WordBase
from ..api.v1.utils import SortOrder

class CRUDWord(CRUDBase[Word, WordCreate, WordBase]):
    def get_by_toki_pona(self, db: Session, *, toki_pona: str) -> Optional[Word]:
        stmt = (
            select(Word)
            .where(Word.toki_pona == toki_pona)
            .options(selectinload(Word.groups))
        )
        return db.execute(stmt).scalar_one_or_none()

    def get_by_group(
        self,
        db: Session,
        *,
        group_id: int,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = "toki_pona",
        order: SortOrder = SortOrder.ASC
    ) -> List[Word]:
        """Get words in a group with sorting and pagination."""
        # Create base query
        stmt = (
            select(Word)
            .join(Word.groups)
            .where(Word.groups.any(id=group_id))
            .options(selectinload(Word.groups))
        )
        
        # Get the column to sort by
        sort_column = getattr(Word, sort_by)
        
        # Apply sort order
        if order == SortOrder.DESC:
            sort_column = desc(sort_column)
        
        # Apply sorting, offset, and limit
        stmt = stmt.order_by(sort_column).offset(skip).limit(limit)
        return list(db.execute(stmt).scalars().all())
    
    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = "toki_pona",
        order: SortOrder = SortOrder.ASC
    ) -> List[Word]:
        """Override get_multi to support sorting."""
        # Create base query
        stmt = select(self.model).options(selectinload(Word.groups))
        
        # Get the column to sort by
        sort_column = getattr(self.model, sort_by)
        
        # Apply sort order
        if order == SortOrder.DESC:
            sort_column = desc(sort_column)
        
        # Apply sorting, offset, and limit
        stmt = stmt.order_by(sort_column).offset(skip).limit(limit)
        return list(db.execute(stmt).scalars().all())
    
    def update_review_counts(self, db: Session, *, word_id: int, correct: bool) -> Word:
        word = self.get(db, id=word_id)
        if correct:
            word.correct_count += 1
        else:
            word.wrong_count += 1
        db.commit()
        return word

crud_word = CRUDWord(Word)
