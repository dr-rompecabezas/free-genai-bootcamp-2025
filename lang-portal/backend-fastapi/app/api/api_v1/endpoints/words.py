from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, asc, desc
from sqlalchemy.exc import IntegrityError

from app.db.base import get_db
from app.models.word import Word
from app.schemas.word import WordCreate, WordUpdate, Word as WordSchema

router = APIRouter()

@router.get("/", response_model=List[WordSchema])
async def read_words(
    page: int = 1,
    sort_key: str = "id",
    sort_direction: str = "asc",
    items_per_page: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve words with pagination and sorting.
    """
    try:
        skip = (page - 1) * items_per_page
        
        # Build the query with sorting
        query = select(Word)
        
        # Add sorting
        if hasattr(Word, sort_key):
            sort_column = getattr(Word, sort_key)
            if sort_direction.lower() == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))
        
        # Add pagination
        query = query.offset(skip).limit(items_per_page)
        
        async with db as session:
            result = await session.execute(query)
            words = result.scalars().all()
            return words
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=WordSchema)
async def create_word(
    word: WordCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create new word.
    """
    try:
        db_word = Word(
            kanji=word.kanji,
            romaji=word.romaji,
            english=word.english,
            parts=word.parts,
            group_id=word.group_id
        )
        db.add(db_word)
        await db.commit()
        await db.refresh(db_word)
        return db_word
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Invalid group_id")

@router.get("/{word_id}", response_model=WordSchema)
async def read_word(
    word_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get word by ID.
    """
    async with db as session:
        result = await session.execute(
            select(Word).filter(Word.id == word_id)
        )
        word = result.scalar_one_or_none()
        
    if word is None:
        raise HTTPException(status_code=404, detail="Word not found")
    return word

@router.put("/{word_id}", response_model=WordSchema)
async def update_word(
    word_id: int,
    word_update: WordUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update a word.
    """
    async with db as session:
        result = await session.execute(
            select(Word).filter(Word.id == word_id)
        )
        word = result.scalar_one_or_none()
        
        if word is None:
            raise HTTPException(status_code=404, detail="Word not found")
        
        # Update word fields if provided
        if word_update.kanji is not None:
            word.kanji = word_update.kanji
        if word_update.romaji is not None:
            word.romaji = word_update.romaji
        if word_update.english is not None:
            word.english = word_update.english
        if word_update.parts is not None:
            word.parts = word_update.parts
        if word_update.group_id is not None:
            word.group_id = word_update.group_id
        
        await session.commit()
        await session.refresh(word)
        return word

@router.delete("/{word_id}")
async def delete_word(
    word_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a word.
    """
    async with db as session:
        result = await session.execute(
            select(Word).filter(Word.id == word_id)
        )
        word = result.scalar_one_or_none()
        
        if word is None:
            raise HTTPException(status_code=404, detail="Word not found")
        
        await session.delete(word)
        await session.commit()
        return {"message": "Word deleted successfully"}
