def test_get_groups(client, sample_group):
    """Test getting list of groups."""
    # Test default parameters
    response = client.get("/api/v1/groups")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Basic Words"
    assert data[0]["words_count"] == 2
    
    # Test pagination
    response = client.get("/api/v1/groups?page=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0  # No groups on second page
    
    # Test sorting by name
    response = client.get("/api/v1/groups?sort_by=name")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Basic Words"
    
    # Test descending order
    response = client.get("/api/v1/groups?sort_by=name&order=desc")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Basic Words"
    
    # Test invalid sort field
    response = client.get("/api/v1/groups?sort_by=invalid")
    assert response.status_code == 422  # Validation error

def test_get_group_words(client, sample_group):
    """Test getting words in a group."""
    # Test default parameters
    response = client.get(f"/api/v1/groups/{sample_group}/words")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["toki_pona"] == "pona"  # Alphabetically first
    assert data[1]["toki_pona"] == "telo"  # Alphabetically second
    
    # Test pagination
    response = client.get(f"/api/v1/groups/{sample_group}/words?page=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0  # No words on second page
    
    # Test sorting by english
    response = client.get(f"/api/v1/groups/{sample_group}/words?sort_by=english")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["english"] == "good"  # "pona"
    assert data[1]["english"] == "water"  # "telo"
    
    # Test descending order
    response = client.get(f"/api/v1/groups/{sample_group}/words?sort_by=toki_pona&order=desc")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["toki_pona"] == "telo"  # Alphabetically higher
    assert data[1]["toki_pona"] == "pona"  # Alphabetically lower
    
    # Test invalid sort field
    response = client.get(f"/api/v1/groups/{sample_group}/words?sort_by=invalid")
    assert response.status_code == 422  # Validation error

def test_get_nonexistent_group_words(client):
    """Test getting words from a non-existent group."""
    response = client.get("/api/v1/groups/999/words")
    assert response.status_code == 404
    assert response.json()["detail"] == "Group not found"

def test_get_group(client, sample_group):
    """Test getting a specific group by ID."""
    # Test getting existing group
    response = client.get(f"/api/v1/groups/{sample_group}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Basic Words"
    assert data["words_count"] == 2
    assert "description" in data
    assert "id" in data

def test_get_nonexistent_group(client):
    """Test getting a non-existent group."""
    response = client.get("/api/v1/groups/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Group not found"
