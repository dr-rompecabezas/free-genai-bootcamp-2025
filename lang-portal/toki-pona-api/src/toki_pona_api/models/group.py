from sqlalchemy import Column, Integer, String, Text, Table, ForeignKey
from sqlalchemy.orm import relationship

from ..db.base import Base

# Association table for many-to-many relationship between words and groups
word_groups = Table(
    "word_groups",
    Base.metadata,
    Column("word_id", Integer, ForeignKey("words.id"), primary_key=True),
    Column("group_id", Integer, ForeignKey("groups.id"), primary_key=True)
)

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text, nullable=True)

    # Relationships
    words = relationship(
        "Word",
        secondary="word_groups",
        back_populates="groups"
    )
    study_sessions = relationship("StudySession", back_populates="group")
