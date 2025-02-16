from typing import List
from sqlalchemy.orm import Session
from datetime import datetime

from .base import CRUDBase
from ..models.study_session import StudySession, StudyActivity, WordReview
from ..schemas.study_session import (
    StudySessionCreate,
    StudySessionBase,
    StudyActivityBase,
    WordReviewCreate,
    WordReviewBase
)

class CRUDStudySession(CRUDBase[StudySession, StudySessionCreate, StudySessionBase]):
    def get_by_group(self, db: Session, *, group_id: int) -> List[StudySession]:
        return (
            db.query(StudySession)
            .filter(StudySession.group_id == group_id)
            .all()
        )

class CRUDStudyActivity(CRUDBase[StudyActivity, StudyActivityBase, StudyActivityBase]):
    def get_by_name(self, db: Session, *, name: str) -> StudyActivity:
        return db.query(StudyActivity).filter(StudyActivity.name == name).first()

class CRUDWordReview(CRUDBase[WordReview, WordReviewCreate, WordReviewBase]):
    def get_by_session(self, db: Session, *, session_id: int) -> List[WordReview]:
        return (
            db.query(WordReview)
            .filter(WordReview.study_session_id == session_id)
            .all()
        )

study_session = CRUDStudySession(StudySession)
study_activity = CRUDStudyActivity(StudyActivity)
word_review = CRUDWordReview(WordReview)
