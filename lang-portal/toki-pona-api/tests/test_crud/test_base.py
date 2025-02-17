import pytest
from typing import Dict, Any
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.toki_pona_api.crud.base import CRUDBase
from src.toki_pona_api.models.word import Word
from src.toki_pona_api.schemas.word import WordCreate, WordBase


# Create a test CRUD class using Word model
class TestCRUD(CRUDBase[Word, WordCreate, WordBase]):
    pass

crud_test = TestCRUD(Word)

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
    # Get existing word
    word = crud_test.get(db_session, id=sample_words[0])
    
    # Test updating with Pydantic model
    update_data = WordBase(
        toki_pona=word.toki_pona,
        english="updated_english",
        definition=word.definition,
        components=word.components
    )
    updated_word = crud_test.update(db_session, db_obj=word, obj_in=update_data)
    assert updated_word.english == "updated_english"
    
    # Test updating with dictionary
    dict_update = {"english": "dict_updated"}
    dict_updated_word = crud_test.update(db_session, db_obj=word, obj_in=dict_update)
    assert dict_updated_word.english == "dict_updated"

def test_remove(db_session, sample_words):
    """Test removing an item."""
    # Remove existing word
    word = crud_test.remove(db_session, id=sample_words[0])
    assert word.id == sample_words[0]
    
    # Verify word is removed
    removed_word = crud_test.get(db_session, id=sample_words[0])
    assert removed_word is None
