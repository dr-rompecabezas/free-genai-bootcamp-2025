# tests/test_crud/test_words.py
from toki_pona_api.crud.words import crud_word

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

def test_update_review_counts(db_session, sample_words):
    """Test updating word review counts."""
    word = sample_words[0]
    initial_correct = word.correct_count
    
    crud_word.update_review_counts(db_session, word_id=word.id, correct=True)
    assert word.correct_count == initial_correct + 1
