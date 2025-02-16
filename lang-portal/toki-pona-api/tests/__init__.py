# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from toki_pona_api.db.base import Base
from toki_pona_api.db.session import get_db
from toki_pona_api.main import app
from toki_pona_api.models.word import WordModel
from toki_pona_api.models.group import GroupModel
from toki_pona_api.models.study_session import StudySessionModel, StudyActivityModel

# Use in-memory SQLite for testing
SQLALCHEMY_TEST_DATABASE_URL = "sqlite://"

@pytest.fixture(scope="session")
def engine():
    engine = create_engine(
        SQLALCHEMY_TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    return engine

@pytest.fixture(scope="function")
def db_session(engine):
    """Creates a fresh database session for each test."""
    TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()

@pytest.fixture(scope="function")
def client(db_session):
    """Creates a test client with a clean database."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

@pytest.fixture
def sample_words(db_session):
    """Creates sample words for testing."""
    words = [
        WordModel(
            toki_pona="telo",
            english="water",
            definition="liquid, fluidity, water",
            components={"root": "telo"}
        ),
        WordModel(
            toki_pona="pona",
            english="good",
            definition="good, simple, positive, nice",
            components={"root": "pona"}
        )
    ]
    for word in words:
        db_session.add(word)
    db_session.commit()
    return words

@pytest.fixture
def sample_group(db_session, sample_words):
    """Creates a sample word group for testing."""
    group = GroupModel(
        name="Basic Words",
        description="Essential Toki Pona vocabulary"
    )
    group.words = sample_words
    db_session.add(group)
    db_session.commit()
    return group

@pytest.fixture
def sample_activity(db_session):
    """Creates a sample study activity for testing."""
    activity = StudyActivityModel(
        name="Flashcards",
        url="/apps/flashcards",
        description="Practice with flashcards"
    )
    db_session.add(activity)
    db_session.commit()
    return activity

# tests/test_api/test_words.py
def test_get_words(client, sample_words):
    """Test getting list of words."""
    response = client.get("/words")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["toki_pona"] == "telo"
    assert data[1]["toki_pona"] == "pona"

def test_get_word(client, sample_words):
    """Test getting a specific word."""
    word_id = sample_words[0].id
    response = client.get(f"/words/{word_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["toki_pona"] == "telo"
    assert data["english"] == "water"

def test_get_nonexistent_word(client):
    """Test getting a word that doesn't exist."""
    response = client.get("/words/999")
    assert response.status_code == 404

# tests/test_api/test_groups.py
def test_get_groups(client, sample_group):
    """Test getting list of groups."""
    response = client.get("/groups")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Basic Words"
    assert data[0]["words_count"] == 2

def test_get_group_words(client, sample_group):
    """Test getting words in a group."""
    response = client.get(f"/groups/{sample_group.id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["toki_pona"] == "telo"

# tests/test_api/test_study_sessions.py
def test_create_study_session(client, sample_group, sample_activity):
    """Test creating a new study session."""
    response = client.post(
        "/study_sessions",
        json={
            "group_id": sample_group.id,
            "study_activity_id": sample_activity.id
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["group_id"] == sample_group.id
    assert data["study_activity_id"] == sample_activity.id

def test_create_word_review(client, sample_words, sample_group, sample_activity):
    """Test creating a word review in a study session."""
    # First create a study session
    session_response = client.post(
        "/study_sessions",
        json={
            "group_id": sample_group.id,
            "study_activity_id": sample_activity.id
        }
    )
    session_id = session_response.json()["id"]
    
    # Then create a review
    review_response = client.post(
        f"/study_sessions/{session_id}/review",
        json={
            "word_id": sample_words[0].id,
            "correct": True
        }
    )
    assert review_response.status_code == 200
    data = review_response.json()
    assert data["word_id"] == sample_words[0].id
    assert data["correct"] == True

# tests/test_crud/test_words.py
from toki_pona_api.crud.words import crud_word

def test_create_word(db_session):
    """Test creating a new word."""
    word_data = {
        "toki_pona": "moku",
        "english": "food",
        "definition": "food, to eat",
        "components": {"root": "moku"}
    }
    word = crud_word.create(db_session, obj_in=word_data)
    assert word.toki_pona == "moku"
    assert word.english == "food"

def test_update_review_counts(db_session, sample_words):
    """Test updating word review counts."""
    word = sample_words[0]
    initial_correct = word.correct_count
    
    crud_word.update_review_counts(db_session, word_id=word.id, correct=True)
    assert word.correct_count == initial_correct + 1
