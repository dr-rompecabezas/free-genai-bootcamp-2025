from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from fastapi import FastAPI, Query, HTTPException
from sqlalchemy.orm import Session
from enum import Enum

# --- CRUD Operations ---

class CRUDBase:
    """Base class for CRUD operations"""
    def __init__(self, model):
        self.model = model

    def get(self, db: Session, id: int):
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = "id",
        order: SortOrder = SortOrder.ASC
    ):
        query = db.query(self.model)
        if hasattr(self.model, sort_by):
            order_field = getattr(self.model, sort_by)
            if order == SortOrder.DESC:
                order_field = order_field.desc()
            query = query.order_by(order_field)
        return query.offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: BaseModel):
        obj_data = obj_in.model_dump()
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

class CRUDWord(CRUDBase):
    def __init__(self):
        super().__init__(WordModel)

    def get_by_toki_pona(self, db: Session, *, toki_pona: str):
        return db.query(self.model).filter(self.model.toki_pona == toki_pona).first()

    def get_by_group(
        self,
        db: Session,
        *,
        group_id: int,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = "toki_pona",
        order: SortOrder = SortOrder.ASC
    ):
        query = db.query(self.model).join(word_groups).filter(word_groups.c.group_id == group_id)
        if hasattr(self.model, sort_by):
            order_field = getattr(self.model, sort_by)
            if order == SortOrder.DESC:
                order_field = order_field.desc()
            query = query.order_by(order_field)
        return query.offset(skip).limit(limit).all()

    def update_review_counts(self, db: Session, *, word_id: int, correct: bool):
        word = self.get(db, word_id)
        if not word:
            raise NotFoundError(f"Word with id {word_id} not found")
        if correct:
            word.correct_count += 1
        else:
            word.wrong_count += 1
        db.commit()
        db.refresh(word)
        return word

class CRUDGroup(CRUDBase):
    def __init__(self):
        super().__init__(GroupModel)

    def get_by_name(self, db: Session, *, name: str):
        return db.query(self.model).filter(self.model.name == name).first()

    def add_word(self, db: Session, *, group_id: int, word_id: int):
        group = self.get(db, group_id)
        word = crud_word.get(db, word_id)
        if not group or not word:
            raise NotFoundError("Group or word not found")
        group.words.append(word)
        group.words_count = len(group.words)
        db.commit()
        db.refresh(group)
        return group

class CRUDStudySession(CRUDBase):
    def __init__(self):
        super().__init__(StudySessionModel)

    def get_session_reviews(self, db: Session, *, session_id: int):
        return db.query(WordReviewModel).filter(
            WordReviewModel.study_session_id == session_id
        ).all()

    def create_review(self, db: Session, *, session_id: int, review: WordReviewCreate):
        # First update the word's review counts
        crud_word.update_review_counts(db, word_id=review.word_id, correct=review.correct)
        
        # Then create the review record
        db_review = WordReviewModel(
            study_session_id=session_id,
            word_id=review.word_id,
            correct=review.correct
        )
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
        return db_review

# Initialize CRUD operations
crud_word = CRUDWord()
crud_group = CRUDGroup()
crud_session = CRUDStudySession()

# --- Updated API Endpoints ---

@app.get("/words", response_model=List[Word])
async def get_words(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    sort_by: str = Query("toki_pona", regex="^(toki_pona|english|correct_count|wrong_count)$"),
    order: SortOrder = Query(SortOrder.ASC),
    db: Session = Depends(get_db)
):
    """
    Get a paginated list of Toki Pona words with review statistics
    """
    skip = (page - 1) * limit
    return crud_word.get_multi(db, skip=skip, limit=limit, sort_by=sort_by, order=order)

@app.get("/words/{word_id}", response_model=Word)
async def get_word(
    word_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific word by ID
    """
    word = crud_word.get(db, word_id)
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    return word

@app.get("/groups", response_model=List[Group])
async def get_groups(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    sort_by: str = Query("name", regex="^(name|words_count)$"),
    order: SortOrder = Query(SortOrder.ASC),
    db: Session = Depends(get_db)
):
    """
    Get a paginated list of word groups
    """
    skip = (page - 1) * limit
    return crud_group.get_multi(db, skip=skip, limit=limit, sort_by=sort_by, order=order)

@app.get("/groups/{group_id}", response_model=List[Word])
async def get_group_words(
    group_id: int,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    sort_by: str = Query("toki_pona", regex="^(toki_pona|english|correct_count|wrong_count)$"),
    order: SortOrder = Query(SortOrder.ASC),
    db: Session = Depends(get_db)
):
    """
    Get words from a specific group
    """
    skip = (page - 1) * limit
    return crud_word.get_by_group(
        db,
        group_id=group_id,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        order=order
    )

@app.post("/study_sessions", response_model=StudySession)
async def create_study_session(
    session: StudySessionCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new study session for a group
    """
    return crud_session.create(db, obj_in=session)

@app.post("/study_sessions/{session_id}/review", response_model=WordReview)
async def create_word_review(
    session_id: int,
    review: WordReviewCreate,
    db: Session = Depends(get_db)
):
    """
    Log a review attempt for a word during a study session
    """
    return crud_session.create_review(db, session_id=session_id, review=review)
