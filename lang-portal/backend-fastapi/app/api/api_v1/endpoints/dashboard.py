from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, text
from datetime import datetime, timedelta
from typing import Optional

from app.db.base import get_db
from app.schemas.dashboard import DashboardStats, RecentSession

router = APIRouter()

@router.get("/recent-session", response_model=Optional[RecentSession])
async def get_recent_session(
    db: AsyncSession = Depends(get_db)
):
    """
    Get the most recent study session with activity stats.
    """
    async with db as session:
        # Using raw SQL for complex query
        query = text("""
            SELECT 
                ss.id,
                ss.group_id,
                ss.started_at as created_at,
                COUNT(CASE WHEN sa.correct = 1 THEN 1 END) as correct_count,
                COUNT(CASE WHEN sa.correct = 0 THEN 1 END) as wrong_count
            FROM study_sessions ss
            LEFT JOIN study_activities sa ON ss.id = sa.session_id
            GROUP BY ss.id
            ORDER BY ss.started_at DESC
            LIMIT 1
        """)
        
        result = await session.execute(query)
        session_data = result.mappings().first()
        
        if not session_data:
            return None
            
        return {
            "id": session_data["id"],
            "group_id": session_data["group_id"],
            "created_at": session_data["created_at"],
            "correct_count": session_data["correct_count"] or 0,
            "wrong_count": session_data["wrong_count"] or 0
        }

@router.get("/stats", response_model=DashboardStats)
async def get_study_stats(
    db: AsyncSession = Depends(get_db)
):
    """
    Get overall learning statistics.
    """
    async with db as session:
        # Total vocabulary count
        vocab_query = select(func.count()).select_from(text("words"))
        result = await session.execute(vocab_query)
        total_vocabulary = result.scalar() or 0

        # Total unique words studied
        unique_words_query = text("""
            SELECT COUNT(DISTINCT word_id) as total_words
            FROM study_activities
        """)
        result = await session.execute(unique_words_query)
        total_words_studied = result.scalar() or 0

        # Mastered words (>80% success rate and at least 5 attempts)
        mastered_query = text("""
            WITH word_stats AS (
                SELECT 
                    word_id,
                    COUNT(*) as total_attempts,
                    SUM(CASE WHEN correct = 1 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) as success_rate
                FROM study_activities
                GROUP BY word_id
                HAVING total_attempts >= 5
            )
            SELECT COUNT(*) as mastered_words
            FROM word_stats
            WHERE success_rate >= 0.8
        """)
        result = await session.execute(mastered_query)
        mastered_words = result.scalar() or 0

        # Overall success rate
        success_rate_query = text("""
            SELECT 
                SUM(CASE WHEN correct = 1 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) as success_rate
            FROM study_activities
        """)
        result = await session.execute(success_rate_query)
        success_rate = result.scalar() or 0

        # Total study sessions
        sessions_query = select(func.count()).select_from(text("study_sessions"))
        result = await session.execute(sessions_query)
        total_sessions = result.scalar() or 0

        # Active groups in last 30 days
        active_groups_query = text("""
            SELECT COUNT(DISTINCT group_id) as active_groups
            FROM study_sessions
            WHERE started_at >= :threshold_date
        """)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        result = await session.execute(
            active_groups_query,
            {"threshold_date": thirty_days_ago}
        )
        active_groups = result.scalar() or 0

        return {
            "total_vocabulary": total_vocabulary,
            "total_words_studied": total_words_studied,
            "mastered_words": mastered_words,
            "success_rate": float(success_rate),
            "total_sessions": total_sessions,
            "active_groups": active_groups
        }
