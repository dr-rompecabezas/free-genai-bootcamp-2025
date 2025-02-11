from pydantic import BaseModel
from datetime import datetime

class RecentSession(BaseModel):
    id: int
    group_id: int
    created_at: datetime
    correct_count: int
    wrong_count: int

class DashboardStats(BaseModel):
    total_vocabulary: int
    total_words_studied: int
    mastered_words: int
    success_rate: float
    total_sessions: int
    active_groups: int
