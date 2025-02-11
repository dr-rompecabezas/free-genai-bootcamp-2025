from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class StudySession(Base):
    __tablename__ = "study_sessions"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"))
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    group = relationship("Group", back_populates="study_sessions")
    activities = relationship("StudyActivity", back_populates="session")

class StudyActivity(Base):
    __tablename__ = "study_activities"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("study_sessions.id"))
    word_id = Column(Integer, ForeignKey("words.id"))
    correct = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    url = Column(String, nullable=True)

    # Relationships
    session = relationship("StudySession", back_populates="activities")
    word = relationship("Word", back_populates="study_activities")
