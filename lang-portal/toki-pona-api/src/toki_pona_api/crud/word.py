from typing import List, Optional
from sqlalchemy.orm import Session

from .base import CRUDBase
from ..models.word import Word
from ..schemas.word import WordCreate, WordBase

class CRUDWord(CRUDBase[Word, WordCreate, WordBase]):
    def get_by_toki_pona(self, db: Session, *, toki_pona: str) -> Optional[Word]:
        return db.query(Word).filter(Word.toki_pona == toki_pona).first()

    def get_by_group(self, db: Session, *, group_id: int) -> List[Word]:
        return (
            db.query(Word)
            .join(Word.groups)
            .filter(Word.groups.any(id=group_id))
            .all()
        )
    
    def update_review_counts(self, db: Session, *, word_id: int, correct: bool) -> Word:
        word = self.get(db, id=word_id)
        if correct:
            word.correct_count += 1
        else:
            word.wrong_count += 1
        db.commit()
        return word

crud_word = CRUDWord(Word)
