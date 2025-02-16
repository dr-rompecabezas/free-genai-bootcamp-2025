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
