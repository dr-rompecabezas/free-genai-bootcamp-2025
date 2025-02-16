from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .word import Word
from .group import Group, word_groups
from .study_session import StudyActivity, StudySession, WordReview

__all__ = [
    "Word",
    "Group",
    "word_groups",
    "StudyActivity",
    "StudySession",
    "WordReview",
    "Base"
]
