from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ....db.session import get_db
from ....schemas.study_session import (
    StudySession,
    StudySessionCreate,
    WordReview,
    WordReviewCreate
)
from ....crud.study_session import study_session, word_review

router = APIRouter()

@router.post("/", response_model=StudySession)
async def create_study_session(
    session: StudySessionCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new study session for a group
    """
    return study_session.create(db=db, obj_in=session)

@router.post("/{session_id}/review", response_model=WordReview)
async def create_word_review(
    session_id: int,
    review: WordReviewCreate,
    db: Session = Depends(get_db)
):
    """
    Log a review attempt for a word during a study session
    """
    # Verify session exists
    if not study_session.get(db=db, id=session_id):
        raise HTTPException(status_code=404, detail="Study session not found")
    
    review_data = WordReviewCreate(
        word_id=review.word_id,
        correct=review.correct,
        study_session_id=session_id
    )
    return word_review.create(db=db, obj_in=review_data)
