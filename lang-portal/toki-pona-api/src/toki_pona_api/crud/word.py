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

word = CRUDWord(Word)
