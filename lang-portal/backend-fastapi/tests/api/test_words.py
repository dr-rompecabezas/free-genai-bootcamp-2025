import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

pytestmark = pytest.mark.asyncio

async def test_create_word(client: AsyncClient, test_group: dict):
    """Test creating a new word."""
    word_data = {
        "kanji": "新しい",
        "romaji": "あたらしい",
        "english": "new",
        "parts": "[]",
        "group_id": test_group["id"]
    }
    response = await client.post("/api/v1/words/", json=word_data)
    assert response.status_code == 200
    data = response.json()
    assert data["kanji"] == word_data["kanji"]
    assert data["romaji"] == word_data["romaji"]
    assert data["english"] == word_data["english"]
    assert data["group_id"] == word_data["group_id"]

async def test_read_word(client: AsyncClient, test_word: dict):
    """Test retrieving a specific word."""
    response = await client.get(f"/api/v1/words/{test_word['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_word["id"]
    assert data["kanji"] == test_word["kanji"]
    assert data["romaji"] == test_word["romaji"]
    assert data["english"] == test_word["english"]
    assert data["group_id"] == test_word["group_id"]

async def test_read_nonexistent_word(client: AsyncClient):
    """Test retrieving a nonexistent word."""
    response = await client.get("/api/v1/words/999")
    assert response.status_code == 404

async def test_read_words(client: AsyncClient, test_word: dict):
    """Test retrieving all words."""
    response = await client.get("/api/v1/words/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert any(word["id"] == test_word["id"] for word in data)

async def test_update_word(client: AsyncClient, test_word: dict):
    """Test updating a word."""
    update_data = {
        "kanji": "更新",
        "romaji": "こうしん",
        "english": "update",
        "parts": "[]"
    }
    response = await client.put(f"/api/v1/words/{test_word['id']}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["kanji"] == update_data["kanji"]
    assert data["romaji"] == update_data["romaji"]
    assert data["english"] == update_data["english"]

async def test_delete_word(client: AsyncClient, test_word: dict):
    """Test deleting a word."""
    response = await client.delete(f"/api/v1/words/{test_word['id']}")
    assert response.status_code == 200
    # Verify the word is deleted
    response = await client.get(f"/api/v1/words/{test_word['id']}")
    assert response.status_code == 404

async def test_create_word_invalid_group(client: AsyncClient):
    """Test creating a word with nonexistent group."""
    word_data = {
        "kanji": "テスト",
        "romaji": "てすと",
        "english": "test",
        "parts": "[]",
        "group_id": 999
    }
    response = await client.post("/api/v1/words/", json=word_data)
    assert response.status_code == 500  # SQLite foreign key violation
