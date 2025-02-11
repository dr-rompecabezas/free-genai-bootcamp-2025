import pytest
import pytest_asyncio
import asyncio
import warnings
from typing import AsyncGenerator, Generator
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy import event

from app.main import app
from app.db.base import Base, get_db
from app.core.config import settings

# Suppress Pydantic V2 warnings
warnings.filterwarnings(
    "ignore",
    message="Support for class-based.*",
    category=DeprecationWarning,
    module="pydantic.*"
)

# Suppress pytest-asyncio warnings
warnings.filterwarnings(
    "ignore",
    message="The event_loop fixture provided by pytest-asyncio has been redefined.*",
    category=DeprecationWarning,
)

# Use in-memory SQLite for testing
TEST_SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    TEST_SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Enable foreign key constraints for SQLite
@event.listens_for(engine.sync_engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

TestingSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

@pytest.fixture(scope="function")
def event_loop() -> Generator:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(autouse=True)
async def setup_db() -> AsyncGenerator:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session

@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db():
        try:
            yield db_session
        finally:
            await db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()

@pytest_asyncio.fixture
async def test_group(db_session: AsyncSession) -> dict:
    """Create a test group."""
    from app.models.group import Group
    group = Group(name="Test Group", description="Test Description")
    db_session.add(group)
    await db_session.commit()
    await db_session.refresh(group)
    return {"id": group.id, "name": group.name, "description": group.description}

@pytest_asyncio.fixture
async def test_word(db_session: AsyncSession, test_group: dict) -> dict:
    """Create a test word."""
    from app.models.word import Word
    word = Word(
        word="テスト",
        reading="てすと",
        meaning="test",
        group_id=test_group["id"]
    )
    db_session.add(word)
    await db_session.commit()
    await db_session.refresh(word)
    return {
        "id": word.id,
        "word": word.word,
        "reading": word.reading,
        "meaning": word.meaning,
        "group_id": word.group_id
    }

@pytest_asyncio.fixture
async def test_study_session(db_session: AsyncSession, test_group: dict) -> dict:
    """Create a test study session."""
    from app.models.study import StudySession
    session = StudySession(group_id=test_group["id"])
    db_session.add(session)
    await db_session.commit()
    await db_session.refresh(session)
    return {"id": session.id, "group_id": session.group_id}
