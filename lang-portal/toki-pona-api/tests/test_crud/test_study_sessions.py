from datetime import datetime

from src.toki_pona_api.crud.study_session import (
    crud_study_session,
    crud_study_activity,
    crud_word_review
)
from src.toki_pona_api.schemas.study_session import (
    StudySessionCreate,
    StudyActivityBase,
    WordReviewCreate
)

def test_create_study_session(db_session, sample_group, sample_activity):
    """Test creating a new study session."""
    session_data = StudySessionCreate(
        group_id=sample_group,
        study_activity_id=sample_activity
    )
    session = crud_study_session.create(db_session, obj_in=session_data)
    assert session.group_id == sample_group
    assert session.study_activity_id == sample_activity
    assert isinstance(session.created_at, datetime)

def test_get_sessions_by_group(db_session, sample_group, sample_activity):
    """Test retrieving study sessions for a specific group."""
    # Create multiple sessions for the same group
    sessions_data = [
        StudySessionCreate(
            group_id=sample_group,
            study_activity_id=sample_activity
        )
        for _ in range(2)
    ]
    for session_data in sessions_data:
        crud_study_session.create(db_session, obj_in=session_data)
    
    # Get sessions for the group
    group_sessions = crud_study_session.get_by_group(db_session, group_id=sample_group)
    assert len(group_sessions) == 2
    assert all(s.group_id == sample_group for s in group_sessions)
    
    # Test with non-existent group
    non_existent_group_sessions = crud_study_session.get_by_group(db_session, group_id=99999)
    assert len(non_existent_group_sessions) == 0

def test_create_study_activity(db_session):
    """Test creating a new study activity."""
    activity_data = StudyActivityBase(
        name="Quiz",
        url="/apps/quiz",
        description="Test your knowledge"
    )
    activity = crud_study_activity.create(db_session, obj_in=activity_data)
    assert activity.name == "Quiz"
    assert activity.url == "/apps/quiz"
    assert activity.description == "Test your knowledge"

def test_get_activity_by_name(db_session, sample_activity):
    """Test retrieving a study activity by name."""
    # Get the actual activity object first
    activity = crud_study_activity.get(db_session, id=sample_activity)
    
    # Test get_by_name
    found_activity = crud_study_activity.get_by_name(db_session, name=activity.name)
    assert found_activity is not None
    assert found_activity.id == sample_activity
    assert found_activity.name == "Flashcards"
    assert found_activity.url == "/apps/flashcards"
    
    # Test with non-existent activity name
    non_existent_activity = crud_study_activity.get_by_name(db_session, name="NonExistentActivity")
    assert non_existent_activity is None

def test_create_word_review(db_session, sample_group, sample_activity, sample_words):
    """Test creating a word review for a study session."""
    # Create a study session first
    session_data = StudySessionCreate(
        group_id=sample_group,
        study_activity_id=sample_activity
    )
    session = crud_study_session.create(db_session, obj_in=session_data)
    
    # Create a word review
    review_data = WordReviewCreate(
        word_id=sample_words[0],
        correct=True
    )
    review = crud_word_review.create(db_session, obj_in=review_data)
    review.study_session_id = session.id  # Set the session ID after creation
    db_session.commit()
    
    assert review.word_id == sample_words[0]
    assert review.correct is True
    assert review.study_session_id == session.id
    assert isinstance(review.created_at, datetime)

def test_get_reviews_by_session(db_session, sample_group, sample_activity, sample_words):
    """Test retrieving word reviews for a specific study session."""
    # Create a study session
    session_data = StudySessionCreate(
        group_id=sample_group,
        study_activity_id=sample_activity
    )
    session = crud_study_session.create(db_session, obj_in=session_data)
    
    # Create multiple reviews for the session
    review_data = [
        WordReviewCreate(word_id=word_id, correct=i % 2 == 0)
        for i, word_id in enumerate(sample_words)
    ]
    for review in review_data:
        word_review = crud_word_review.create(db_session, obj_in=review)
        word_review.study_session_id = session.id
    db_session.commit()
    
    # Get reviews for the session
    session_reviews = crud_word_review.get_by_session(db_session, session_id=session.id)
    assert len(session_reviews) == len(sample_words)
    assert all(r.study_session_id == session.id for r in session_reviews)
    
    # Test with non-existent session
    non_existent_session_reviews = crud_word_review.get_by_session(db_session, session_id=99999)
    assert len(non_existent_session_reviews) == 0