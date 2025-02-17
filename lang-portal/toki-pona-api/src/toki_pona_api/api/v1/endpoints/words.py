from typing import List
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from ....db.session import get_db
from ....schemas.word import Word
from ....crud.word import crud_word
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
    return crud_word.get_multi(db=db, skip=skip, limit=100)

@router.get("/{word_id}", response_model=Word)
async def get_word(
    word_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific word by ID
    """
    word = crud_word.get(db=db, id=word_id)
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    return word
