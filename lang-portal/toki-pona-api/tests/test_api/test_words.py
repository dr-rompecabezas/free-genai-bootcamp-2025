def test_get_words(client, sample_words):
    """Test getting list of words."""
    # Test default parameters
    response = client.get("/api/v1/words")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["toki_pona"] == "pona"  # Alphabetically first
    assert data[1]["toki_pona"] == "telo"  # Alphabetically second
    
    # Test pagination
    response = client.get("/api/v1/words?page=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0  # No words on second page
    
    # Test sorting by different fields
    response = client.get("/api/v1/words?sort_by=english")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["english"] == "good"  # "pona"
    assert data[1]["english"] == "water"  # "telo"
    
    # Test sorting by review counts
    response = client.get("/api/v1/words?sort_by=correct_count")
    assert response.status_code == 200
    
    # Test descending order
    response = client.get("/api/v1/words?sort_by=toki_pona&order=desc")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["toki_pona"] == "telo"  # Alphabetically higher
    assert data[1]["toki_pona"] == "pona"  # Alphabetically lower
    
    # Test invalid sort field
    response = client.get("/api/v1/words?sort_by=invalid")
    assert response.status_code == 422  # Validation error

def test_get_word(client, sample_words):
    """Test getting a specific word."""
    word_id = sample_words[0]
    response = client.get(f"/api/v1/words/{word_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["toki_pona"] == "telo"
    assert data["english"] == "water"

def test_get_nonexistent_word(client):
    """Test getting a word that doesn't exist."""
    response = client.get("/api/v1/words/999")
    assert response.status_code == 404
