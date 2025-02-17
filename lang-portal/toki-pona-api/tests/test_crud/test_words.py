from src.toki_pona_api.crud import crud_word
from src.toki_pona_api.models import Word

def test_create_word(db_session):
    """Test creating a new word."""
    word_data = {
        "toki_pona": "moku",
        "english": "food",
        "definition": "food, to eat",
        "components": {"root": "moku"}
    }
    word = crud_word.create(db_session, obj_in=word_data)
    assert word.toki_pona == "moku"
    assert word.english == "food"

def test_get_by_toki_pona(db_session, sample_words):
    """Test retrieving a word by its toki pona name."""
    # Get the actual word object first
    word = crud_word.get(db_session, id=sample_words[0])
    
    # Test get_by_toki_pona
    found_word = crud_word.get_by_toki_pona(db_session, toki_pona=word.toki_pona)
    assert found_word is not None
    assert found_word.id == sample_words[0]
    assert found_word.toki_pona == word.toki_pona
    
    # Test with non-existent word
    non_existent_word = crud_word.get_by_toki_pona(db_session, toki_pona="nonexistentword")
    assert non_existent_word is None

def test_get_by_group(db_session, sample_group, sample_words):
    """Test retrieving words by group ID."""
    # Get words for the group
    group_words = crud_word.get_by_group(db_session, group_id=sample_group)
    assert len(group_words) > 0
    assert all(word.id in sample_words for word in group_words)
    
    # Test with non-existent group
    non_existent_group_words = crud_word.get_by_group(db_session, group_id=99999)
    assert len(non_existent_group_words) == 0

def test_update_review_counts(db_session, sample_words):
    """Test updating word review counts using the CRUD method."""
    word_id = sample_words[0]
    word = crud_word.get(db_session, id=word_id)
    initial_correct = word.correct_count
    initial_wrong = word.wrong_count
    
    # Test correct review
    updated_word = crud_word.update_review_counts(db_session, word_id=word_id, correct=True)
    assert updated_word.correct_count == initial_correct + 1
    assert updated_word.wrong_count == initial_wrong
    
    # Test incorrect review
    updated_word = crud_word.update_review_counts(db_session, word_id=word_id, correct=False)
    assert updated_word.correct_count == initial_correct + 1
    assert updated_word.wrong_count == initial_wrong + 1
