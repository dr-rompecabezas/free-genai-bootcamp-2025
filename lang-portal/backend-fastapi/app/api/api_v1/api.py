from fastapi import APIRouter
from app.api.api_v1.endpoints import words, groups, study, dashboard

api_router = APIRouter()

api_router.include_router(words.router, prefix="/words", tags=["words"])
api_router.include_router(groups.router, prefix="/groups", tags=["groups"])
api_router.include_router(study.router, prefix="/study", tags=["study"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
