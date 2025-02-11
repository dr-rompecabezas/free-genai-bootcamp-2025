from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.db.base import get_db
from app.models.word import Word
from app.schemas.word import WordCreate, WordUpdate, Word as WordSchema

router = APIRouter()

@router.get("/", response_model=List[WordSchema])
async def read_words(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve words.
    """
    async with db as session:
        result = await session.execute(
            select(Word).offset(skip).limit(limit)
        )
        words = result.scalars().all()
        return words

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
            word=word.word,
            reading=word.reading,
            meaning=word.meaning,
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
        db_word = result.scalar_one_or_none()
        
        if db_word is None:
            raise HTTPException(status_code=404, detail="Word not found")
            
        update_data = word_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_word, field, value)
            
        try:
            await session.commit()
            await session.refresh(db_word)
            return db_word
        except IntegrityError:
            await session.rollback()
            raise HTTPException(status_code=500, detail="Invalid group_id")

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
        
    return {"ok": True}
