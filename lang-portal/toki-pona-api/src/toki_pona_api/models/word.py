from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import relationship

from ..db.base import Base

class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    toki_pona = Column(String, unique=True, index=True)
    english = Column(String)
    definition = Column(String)
    components = Column(JSON, default={})
    correct_count = Column(Integer, default=0)
    wrong_count = Column(Integer, default=0)

    # Relationships
    word_reviews = relationship("WordReview", back_populates="word")
    groups = relationship(
        "Group",
        secondary="word_groups",
        back_populates="words"
    )
