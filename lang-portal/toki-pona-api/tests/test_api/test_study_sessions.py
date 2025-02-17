def test_create_study_session(client, sample_group, sample_activity):
    """Test creating a new study session."""
    response = client.post(
        "/api/v1/study-sessions",
        json={
            "group_id": sample_group,
            "study_activity_id": sample_activity
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["group_id"] == sample_group
    assert data["study_activity_id"] == sample_activity

def test_create_word_review(client, sample_words, sample_group, sample_activity):
    """Test creating a word review in a study session."""
    # First create a study session
    session_response = client.post(
        "/api/v1/study-sessions",
        json={
            "group_id": sample_group,
            "study_activity_id": sample_activity
        }
    )
    assert session_response.status_code == 200
    assert "id" in session_response.json()
    session_id = session_response.json()["id"]
    
    # Then create a review
    review_response = client.post(
        f"/api/v1/study-sessions/{session_id}/review",
        json={
            "word_id": sample_words[0],
            "correct": True
        }
    )
    assert review_response.status_code == 200
    data = review_response.json()
    assert data["word_id"] == sample_words[0]
    assert data["study_session_id"] == session_id
    assert data["correct"] == True
