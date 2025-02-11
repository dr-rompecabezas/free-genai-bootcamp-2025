import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

pytestmark = pytest.mark.asyncio

async def test_create_study_session(client: AsyncClient, test_group: dict):
    """Test creating a new study session."""
    session_data = {
        "group_id": test_group["id"]
    }
    response = await client.post("/api/v1/study/sessions/", json=session_data)
    assert response.status_code == 200
    data = response.json()
    assert data["group_id"] == session_data["group_id"]
    assert "id" in data
    assert "started_at" in data
    assert data["completed_at"] is None

async def test_read_study_session(client: AsyncClient, test_study_session: dict):
    """Test retrieving a study session by ID."""
    response = await client.get(f"/api/v1/study/sessions/{test_study_session['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_study_session["id"]
    assert data["group_id"] == test_study_session["group_id"]

async def test_complete_study_session(client: AsyncClient, test_study_session: dict):
    """Test marking a study session as complete."""
    response = await client.put(f"/api/v1/study/sessions/{test_study_session['id']}/complete")
    assert response.status_code == 200
    
    # Verify session is marked as complete
    response = await client.get(f"/api/v1/study/sessions/{test_study_session['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["completed_at"] is not None

async def test_create_study_activity(
    client: AsyncClient,
    test_study_session: dict,
    test_word: dict
):
    """Test recording a study activity."""
    activity_data = {
        "session_id": test_study_session["id"],
        "word_id": test_word["id"],
        "correct": True,
        "url": "https://example.com/study/1"
    }
    response = await client.post("/api/v1/study/activities/", json=activity_data)
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == activity_data["session_id"]
    assert data["word_id"] == activity_data["word_id"]
    assert data["correct"] == activity_data["correct"]
    assert data["url"] == activity_data["url"]
    assert "id" in data
    assert "created_at" in data

async def test_read_session_activities(
    client: AsyncClient,
    test_study_session: dict,
    test_word: dict
):
    """Test retrieving activities for a study session."""
    # First create an activity
    activity_data = {
        "session_id": test_study_session["id"],
        "word_id": test_word["id"],
        "correct": True
    }
    await client.post("/api/v1/study/activities/", json=activity_data)
    
    # Then retrieve activities
    response = await client.get(f"/api/v1/study/activities/session/{test_study_session['id']}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["session_id"] == test_study_session["id"]

async def test_create_activity_invalid_session(client: AsyncClient, test_word: dict):
    """Test creating an activity with nonexistent session."""
    activity_data = {
        "session_id": 999,
        "word_id": test_word["id"],
        "correct": True
    }
    response = await client.post("/api/v1/study/activities/", json=activity_data)
    assert response.status_code == 500  # SQLite foreign key violation

async def test_create_activity_invalid_word(client: AsyncClient, test_study_session: dict):
    """Test creating an activity with nonexistent word."""
    activity_data = {
        "session_id": test_study_session["id"],
        "word_id": 999,
        "correct": True
    }
    response = await client.post("/api/v1/study/activities/", json=activity_data)
    assert response.status_code == 500  # SQLite foreign key violation
