from fastapi import APIRouter
from .endpoints import words, groups, study_sessions

api_router = APIRouter()

api_router.include_router(words.router, prefix="/words", tags=["Words"])
api_router.include_router(groups.router, prefix="/groups", tags=["Groups"])
api_router.include_router(study_sessions.router, prefix="/study-sessions", tags=["Study Sessions"])
