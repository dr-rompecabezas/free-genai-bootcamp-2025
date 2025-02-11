from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, Boolean, String
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base import Base

class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    kanji = Column(Text, nullable=False, index=True)
    romaji = Column(Text, nullable=False)
    english = Column(Text, nullable=False)
    parts = Column(Text, nullable=False)  # Store parts as JSON string
    group_id = Column(Integer, ForeignKey("groups.id", ondelete="CASCADE"))

    # Relationships
    group = relationship("Group", back_populates="words")
    study_activities = relationship("StudyActivity", back_populates="word")

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False, index=True)
    description = Column(Text, nullable=True)
    words_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    words = relationship("Word", back_populates="group", cascade="all, delete-orphan")
    study_sessions = relationship("StudySession", back_populates="group", cascade="all, delete-orphan")

class StudySession(Base):
    __tablename__ = "study_sessions"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id", ondelete="CASCADE"))
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    group = relationship("Group", back_populates="study_sessions")
    activities = relationship("StudyActivity", back_populates="session", cascade="all, delete-orphan")

class StudyActivity(Base):
    __tablename__ = "study_activities"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("study_sessions.id", ondelete="CASCADE"))
    word_id = Column(Integer, ForeignKey("words.id", ondelete="CASCADE"))
    correct = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    url = Column(String, nullable=True)

    # Relationships
    session = relationship("StudySession", back_populates="activities")
    word = relationship("Word", back_populates="study_activities")
