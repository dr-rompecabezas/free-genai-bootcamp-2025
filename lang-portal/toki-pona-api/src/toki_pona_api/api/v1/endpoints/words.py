from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ....db.session import get_db
from ....schemas.word import Word
from ....crud.word import word
from ..utils import SortOrder

router = APIRouter()

@router.get("/", response_model=List[Word])
async def get_words(
    page: int = Query(1, ge=1),
    sort_by: str = Query("toki_pona", regex="^(toki_pona|english|correct_count|wrong_count)$"),
    order: SortOrder = Query(SortOrder.ASC),
    db: Session = Depends(get_db)
):
    """
    Get a paginated list of Toki Pona words with review statistics
    """
    skip = (page - 1) * 100
    return word.get_multi(db=db, skip=skip, limit=100)
