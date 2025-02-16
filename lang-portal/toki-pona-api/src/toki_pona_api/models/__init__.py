from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from fastapi import FastAPI, Query, HTTPException, Depends
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON, Table
from sqlalchemy.orm import Session, relationship, DeclarativeBase
from sqlalchemy.sql import func
from enum import Enum

# --- SQLAlchemy Setup ---

class Base(DeclarativeBase):
    pass

# Association table for many-to-many relationship between words and groups
word_groups = Table(
    'word_groups',
    Base.metadata,
    Column('word_id', Integer, ForeignKey('words.id', ondelete='CASCADE')),
    Column('group_id', Integer, ForeignKey('groups.id', ondelete='CASCADE'))
)

# --- SQLAlchemy Models ---

class WordModel(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    toki_pona = Column(String, nullable=False, index=True)
    english = Column(String, nullable=False)
    definition = Column(String, nullable=False)
    components = Column(JSON, nullable=False, default=dict)
    correct_count = Column(Integer, default=0)
    wrong_count = Column(Integer, default=0)

    # Relationships
    groups = relationship("GroupModel", secondary=word_groups, back_populates="words")
    reviews = relationship("WordReviewModel", back_populates="word")

class GroupModel(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(String)
    words_count = Column(Integer, default=0)

    # Relationships
    words = relationship("WordModel", secondary=word_groups, back_populates="groups")
    study_sessions = relationship("StudySessionModel", back_populates="group")

class StudyActivityModel(Base):
    __tablename__ = "study_activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    description = Column(String)

    # Relationships
    sessions = relationship("StudySessionModel", back_populates="activity")

class StudySessionModel(Base):
    __tablename__ = "study_sessions"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id", ondelete="CASCADE"))
    study_activity_id = Column(Integer, ForeignKey("study_activities.id", ondelete="CASCADE"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    group = relationship("GroupModel", back_populates="study_sessions")
    activity = relationship("StudyActivityModel", back_populates="sessions")
    reviews = relationship("WordReviewModel", back_populates="session")

class WordReviewModel(Base):
    __tablename__ = "word_review_items"

    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("words.id", ondelete="CASCADE"))
    study_session_id = Column(Integer, ForeignKey("study_sessions.id", ondelete="CASCADE"))
    correct = Column(Boolean, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    word = relationship("WordModel", back_populates="reviews")
    session = relationship("StudySessionModel", back_populates="reviews")
