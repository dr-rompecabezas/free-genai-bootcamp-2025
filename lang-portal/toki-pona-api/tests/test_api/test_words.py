from src.toki_pona_api.crud.word import word

def test_get_words(client, sample_words):
    """Test getting list of words."""
    response = client.get("/api/v1/words")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["toki_pona"] == "telo"
    assert data[1]["toki_pona"] == "pona"

def test_get_word(client, sample_words):
    """Test getting a specific word."""
    word_id = sample_words[0].id
    response = client.get(f"/api/v1/words/{word_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["toki_pona"] == "telo"
    assert data["english"] == "water"

def test_get_nonexistent_word(client):
    """Test getting a word that doesn't exist."""
    response = client.get("/api/v1/words/999")
    assert response.status_code == 404
