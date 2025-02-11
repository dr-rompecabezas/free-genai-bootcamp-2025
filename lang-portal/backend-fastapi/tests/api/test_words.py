import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

pytestmark = pytest.mark.asyncio

async def test_create_word(client: AsyncClient, test_group: dict):
    """Test creating a new word."""
    word_data = {
        "word": "新しい",
        "reading": "あたらしい",
        "meaning": "new",
        "group_id": test_group["id"]
    }
    response = await client.post("/api/v1/words/", json=word_data)
    assert response.status_code == 200
    data = response.json()
    assert data["word"] == word_data["word"]
    assert data["reading"] == word_data["reading"]
    assert data["meaning"] == word_data["meaning"]
    assert "id" in data
    assert "created_at" in data

async def test_read_word(client: AsyncClient, test_word: dict):
    """Test retrieving a word by ID."""
    response = await client.get(f"/api/v1/words/{test_word['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["word"] == test_word["word"]
    assert data["reading"] == test_word["reading"]
    assert data["meaning"] == test_word["meaning"]

async def test_read_nonexistent_word(client: AsyncClient):
    """Test retrieving a nonexistent word."""
    response = await client.get("/api/v1/words/999")
    assert response.status_code == 404

async def test_read_words(client: AsyncClient, test_word: dict):
    """Test retrieving a list of words."""
    response = await client.get("/api/v1/words/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert any(w["id"] == test_word["id"] for w in data)

async def test_update_word(client: AsyncClient, test_word: dict):
    """Test updating a word."""
    update_data = {
        "meaning": "updated meaning"
    }
    response = await client.put(f"/api/v1/words/{test_word['id']}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["meaning"] == update_data["meaning"]
    assert data["word"] == test_word["word"]  # Other fields should remain unchanged

async def test_delete_word(client: AsyncClient, test_word: dict):
    """Test deleting a word."""
    response = await client.delete(f"/api/v1/words/{test_word['id']}")
    assert response.status_code == 200
    
    # Verify word is deleted
    response = await client.get(f"/api/v1/words/{test_word['id']}")
    assert response.status_code == 404

async def test_create_word_invalid_group(client: AsyncClient):
    """Test creating a word with nonexistent group."""
    word_data = {
        "word": "テスト",
        "reading": "てすと",
        "meaning": "test",
        "group_id": 999
    }
    response = await client.post("/api/v1/words/", json=word_data)
    assert response.status_code == 500  # SQLite foreign key violation
