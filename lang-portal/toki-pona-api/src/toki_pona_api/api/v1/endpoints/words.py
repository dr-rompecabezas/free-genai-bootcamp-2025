from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ....db.session import get_db
from ....schemas.word import WordCreate, Word
from ....crud import words

router = APIRouter()

@router.get("/", response_model=List[Word])
def read_words(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieve words.
    """
    return words.get_multi(db, skip=skip, limit=limit)

@router.post("/", response_model=Word)
def create_word(
    *,
    db: Session = Depends(get_db),
    word_in: WordCreate
):
    """
    Create new word.
    """
    return words.create(db=db, obj_in=word_in)
