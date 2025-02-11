from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from app.db.base import get_db
from app.models.study import StudySession, StudyActivity
from app.schemas.study import (
    StudySessionCreate,
    StudySessionUpdate,
    StudySession as StudySessionSchema,
    StudyActivityCreate,
    StudyActivity as StudyActivitySchema
)

router = APIRouter()

@router.post("/sessions/", response_model=StudySessionSchema)
async def create_study_session(
    session: StudySessionCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new study session.
    """
    try:
        db_session = StudySession(group_id=session.group_id)
        db.add(db_session)
        await db.commit()
        await db.refresh(db_session)
        return db_session
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Invalid group_id")

@router.get("/sessions/{session_id}", response_model=StudySessionSchema)
async def read_study_session(
    session_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get study session by ID.
    """
    async with db as session:
        result = await session.execute(
            select(StudySession).filter(StudySession.id == session_id)
        )
        study_session = result.scalar_one_or_none()
        
    if study_session is None:
        raise HTTPException(status_code=404, detail="Study session not found")
    return study_session

@router.put("/sessions/{session_id}/complete")
async def complete_study_session(
    session_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Mark a study session as complete.
    """
    async with db as session:
        result = await session.execute(
            select(StudySession).filter(StudySession.id == session_id)
        )
        study_session = result.scalar_one_or_none()
        
        if study_session is None:
            raise HTTPException(status_code=404, detail="Study session not found")
            
        study_session.completed_at = datetime.utcnow()
        await session.commit()
        await session.refresh(study_session)
        
    return {"ok": True}

@router.post("/activities/", response_model=StudyActivitySchema)
async def create_study_activity(
    activity: StudyActivityCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Record a study activity.
    """
    try:
        db_activity = StudyActivity(
            session_id=activity.session_id,
            word_id=activity.word_id,
            correct=activity.correct,
            url=activity.url
        )
        db.add(db_activity)
        await db.commit()
        await db.refresh(db_activity)
        return db_activity
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Invalid session_id or word_id")

@router.get("/activities/session/{session_id}", response_model=List[StudyActivitySchema])
async def read_session_activities(
    session_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get all activities for a study session.
    """
    async with db as session:
        result = await session.execute(
            select(StudyActivity)
            .filter(StudyActivity.session_id == session_id)
            .order_by(StudyActivity.created_at)
        )
        activities = result.scalars().all()
    return activities
