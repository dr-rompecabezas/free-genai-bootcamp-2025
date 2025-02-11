import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

pytestmark = pytest.mark.asyncio

async def test_get_recent_session_empty(client: AsyncClient):
    """Test getting recent session when no sessions exist."""
    response = await client.get("/api/v1/dashboard/recent-session")
    assert response.status_code == 200
    assert response.json() is None

async def test_get_recent_session(
    client: AsyncClient,
    test_study_session: dict,
    test_word: dict
):
    """Test getting recent session with activity stats."""
    # Create some activities
    activity_data = {
        "session_id": test_study_session["id"],
        "word_id": test_word["id"],
        "correct": True
    }
    await client.post("/api/v1/study/activities/", json=activity_data)
    
    # Create another activity with incorrect answer
    activity_data["correct"] = False
    await client.post("/api/v1/study/activities/", json=activity_data)
    
    response = await client.get("/api/v1/dashboard/recent-session")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_study_session["id"]
    assert data["group_id"] == test_study_session["group_id"]
    assert data["correct_count"] == 1
    assert data["wrong_count"] == 1
    assert "created_at" in data

async def test_get_study_stats_empty(client: AsyncClient):
    """Test getting study stats when no data exists."""
    response = await client.get("/api/v1/dashboard/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["total_vocabulary"] == 0
    assert data["total_words_studied"] == 0
    assert data["mastered_words"] == 0
    assert data["success_rate"] == 0
    assert data["total_sessions"] == 0
    assert data["active_groups"] == 0

async def test_get_study_stats(
    client: AsyncClient,
    test_study_session: dict,
    test_word: dict
):
    """Test getting study stats with existing data."""
    # Create multiple activities for the same word to test mastery
    activity_data = {
        "session_id": test_study_session["id"],
        "word_id": test_word["id"],
        "correct": True
    }
    
    # Create 5 activities with 4 correct answers (80% success rate)
    for _ in range(4):
        await client.post("/api/v1/study/activities/", json=activity_data)
    
    activity_data["correct"] = False
    await client.post("/api/v1/study/activities/", json=activity_data)
    
    response = await client.get("/api/v1/dashboard/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["total_vocabulary"] >= 1  # At least our test word
    assert data["total_words_studied"] == 1
    assert data["mastered_words"] == 1  # 80% success rate meets mastery criteria
    assert abs(data["success_rate"] - 0.8) < 0.01  # Should be close to 0.8
    assert data["total_sessions"] >= 1
    assert data["active_groups"] >= 1
