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

def test_update_review_counts(db_session, sample_words):
    """Test updating word review counts."""
    # Get the actual word object from the database
    word = db_session.query(Word).filter_by(id=sample_words[0]).first()
    
    initial_correct = word.correct_count
    initial_wrong = word.wrong_count
    
    # Update counts
    word.correct_count += 1
    word.wrong_count += 1
    db_session.commit()
    
    # Refresh from DB
    db_session.refresh(word)
    
    assert word.correct_count == initial_correct + 1
    assert word.wrong_count == initial_wrong + 1
