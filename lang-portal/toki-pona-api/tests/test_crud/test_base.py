import pytest

from src.toki_pona_api.crud.base import CRUDBase
from src.toki_pona_api.models.word import Word
from src.toki_pona_api.schemas.word import WordCreate, WordBase


# Create a test CRUD class using Word model
crud_test = CRUDBase[Word, WordCreate, WordBase](Word)

def test_get(db_session, sample_words):
    """Test retrieving a single item by ID."""
    # Test with existing word
    word = crud_test.get(db_session, id=sample_words[0])
    assert word is not None
    assert word.id == sample_words[0]
    
    # Test with non-existent word
    non_existent_word = crud_test.get(db_session, id=99999)
    assert non_existent_word is None

def test_get_multi(db_session, sample_words):
    """Test retrieving multiple items with pagination."""
    # Test default pagination
    words = crud_test.get_multi(db_session)
    assert len(words) >= 2  # We have at least 2 sample words
    
    # Test with custom skip and limit
    words_page = crud_test.get_multi(db_session, skip=1, limit=1)
    assert len(words_page) == 1
    
    # Test with skip > total items
    empty_words = crud_test.get_multi(db_session, skip=100)
    assert len(empty_words) == 0

def test_create(db_session):
    """Test creating a new item."""
    word_data = WordCreate(
        toki_pona="moku",
        english="food",
        definition="food, to eat",
        components={"root": "moku"}
    )
    word = crud_test.create(db_session, obj_in=word_data)
    assert word.toki_pona == "moku"
    assert word.english == "food"
    assert word.definition == "food, to eat"
    assert word.components == {"root": "moku"}

def test_update(db_session, sample_words):
    """Test updating an item."""
    # Get an existing word
    word = crud_test.get(db_session, id=sample_words[0])
    
    # Update with Pydantic model
    update_data = WordBase(
        toki_pona="ilo",
        english="tool",
        definition="tool, machine, device",
        components={"root": "ilo"}
    )
    updated_word = crud_test.update(db_session, db_obj=word, obj_in=update_data)
    assert updated_word.toki_pona == "ilo"
    assert updated_word.english == "tool"
    
    # Update with dict
    update_dict = {"toki_pona": "tomo", "english": "house"}
    updated_word = crud_test.update(db_session, db_obj=word, obj_in=update_dict)
    assert updated_word.toki_pona == "tomo"
    assert updated_word.english == "house"
    # Previous fields should remain unchanged if not in update dict
    assert updated_word.definition == "tool, machine, device"

def test_remove(db_session, sample_words):
    """Test removing an item."""
    # Test with existing word
    word = crud_test.remove(db_session, id=sample_words[0])
    assert word.id == sample_words[0]
    
    # Verify word was removed
    deleted_word = crud_test.get(db_session, id=sample_words[0])
    assert deleted_word is None
    
    # Test with non-existent word
    with pytest.raises(ValueError):
        crud_test.remove(db_session, id=99999)
