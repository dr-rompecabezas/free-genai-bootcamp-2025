from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, index=True)
    reading = Column(String)
    meaning = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    group_id = Column(Integer, ForeignKey("groups.id"))

    # Relationships
    group = relationship("Group", back_populates="words")
    study_activities = relationship("StudyActivity", back_populates="word")
