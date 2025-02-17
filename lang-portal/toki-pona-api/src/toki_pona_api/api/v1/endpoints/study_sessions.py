from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ....db.session import get_db
from ....schemas.study_session import (
    StudySession,
    StudySessionCreate,
    WordReview,
    WordReviewCreate
)
from ....crud.study_session import crud_study_session, crud_word_review

router = APIRouter()

@router.post("/", response_model=StudySession)
async def create_study_session(
    session: StudySessionCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new study session for a group
    """
    return crud_study_session.create(db=db, obj_in=session)

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
    if not crud_study_session.get(db=db, id=session_id):
        raise HTTPException(status_code=404, detail="Study session not found")
    
    # Create review with session_id included in the input data
    review_dict = review.model_dump()
    review_dict["study_session_id"] = session_id
    
    return crud_word_review.create(db=db, obj_in=review_dict)
