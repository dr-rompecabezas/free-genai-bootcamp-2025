from typing import List
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from ....dependencies import get_db
from ....schemas.word import Word
from ....crud.word import crud_word
from ..utils import SortOrder
from ....config import settings

router = APIRouter()

@router.get("/", response_model=List[Word])
async def get_words(
    page: int = Query(1, ge=1),
    sort_by: str = Query("toki_pona", pattern="^(toki_pona|english|correct_count|wrong_count)$"),
    order: SortOrder = Query(SortOrder.ASC),
    db: Session = Depends(get_db)
):
    """
    Get a paginated list of words
    """
    skip = (page - 1) * settings.PAGE_SIZE
    return crud_word.get_multi(
        db,
        skip=skip,
        limit=settings.PAGE_SIZE,
        sort_by=sort_by,
        order=order
    )

@router.get("/{word_id}", response_model=Word)
async def get_word(word_id: int, db: Session = Depends(get_db)):
    """
    Get a specific word by ID
    """
    word = crud_word.get(db=db, id=word_id)
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    return word
