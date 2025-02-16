from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

from ..db.base import Base

class StudyActivity(Base):
    __tablename__ = "study_activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    url = Column(String)
    description = Column(Text)

    # Relationships
    study_sessions = relationship("StudySession", back_populates="study_activity")

class StudySession(Base):
    __tablename__ = "study_sessions"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"))
    study_activity_id = Column(Integer, ForeignKey("study_activities.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    group = relationship("Group", back_populates="study_sessions")
    study_activity = relationship("StudyActivity", back_populates="study_sessions")
    word_reviews = relationship("WordReview", back_populates="study_session")

class WordReview(Base):
    __tablename__ = "word_reviews"

    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("words.id"))
    study_session_id = Column(Integer, ForeignKey("study_sessions.id"))
    correct = Column(Boolean)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    word = relationship("Word", back_populates="word_reviews")
    study_session = relationship("StudySession", back_populates="word_reviews")
