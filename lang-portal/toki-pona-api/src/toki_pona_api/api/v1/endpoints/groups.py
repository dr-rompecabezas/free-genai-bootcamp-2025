from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ....db.session import get_db
from ....schemas.group import Group
from ....schemas.word import Word
from ....crud.group import crud_group
from ....crud.word import crud_word
from ..utils import SortOrder
from ....config import settings

router = APIRouter()

@router.get("/", response_model=List[Group])
async def get_groups(
    page: int = Query(1, ge=1),
    sort_by: str = Query("name", regex="^(name|words_count)$"),
    order: SortOrder = Query(SortOrder.ASC),
    db: Session = Depends(get_db)
):
    """
    Get a paginated list of word groups
    """
    skip = (page - 1) * settings.PAGE_SIZE
    groups = crud_group.get_multi(
        db,
        skip=skip,
        limit=settings.PAGE_SIZE
    )
    
    return [
        Group(
            id=group.id,
            name=group.name,
            description=group.description,
            words_count=len(group.words)
        )
        for group in groups
    ]

@router.get("/{group_id}/words", response_model=List[Word])
async def get_group_words(
    group_id: int,
    page: int = Query(1, ge=1),
    sort_by: str = Query("toki_pona", regex="^(toki_pona|english|correct_count|wrong_count)$"),
    order: SortOrder = Query(SortOrder.ASC),
    db: Session = Depends(get_db)
):
    """
    Get words from a specific group
    """
    return crud_word.get_by_group(db=db, group_id=group_id)
