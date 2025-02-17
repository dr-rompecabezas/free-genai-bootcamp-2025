import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.toki_pona_api.db.base import Base
from src.toki_pona_api.db.session import get_db
from src.toki_pona_api.main import app
from src.toki_pona_api.models.word import Word
from src.toki_pona_api.models.group import Group
from src.toki_pona_api.models.study_session import StudyActivity, StudySession

# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite://"

@pytest.fixture(scope="session")
def engine():
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
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

@pytest.fixture(autouse=True)
def clean_tables(db_session):
    """Clean all tables before each test."""
    for table in Base.metadata.sorted_tables:
        db_session.execute(table.delete())
    db_session.commit()

@pytest.fixture(scope="function")
def client(db_session):
    """Creates a test client with a clean database."""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

@pytest.fixture
def sample_words(db_session):
    """Creates sample words for testing."""
    words = [
        Word(
            toki_pona="telo",
            english="water",
            definition="liquid, fluidity, water",
            components={"root": "telo"}
        ),
        Word(
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
    # First create the group
    group = Group(
        name="Basic Words",
        description="Essential Toki Pona vocabulary"
    )
    db_session.add(group)
    db_session.flush()  # Get the group ID
    
    # Add words explicitly
    for word in sample_words:
        group.words.append(word)
    
    db_session.commit()
    db_session.refresh(group)
    
    # Verify relationship
    assert len(group.words) == 2, f"Group has {len(group.words)} words instead of 2"
    return group

@pytest.fixture
def sample_activity(db_session):
    """Creates a sample study activity for testing."""
    activity = StudyActivity(
        name="Flashcards",
        url="/apps/flashcards",
        description="Practice with flashcards"
    )
    db_session.add(activity)
    db_session.commit()
    return activity
