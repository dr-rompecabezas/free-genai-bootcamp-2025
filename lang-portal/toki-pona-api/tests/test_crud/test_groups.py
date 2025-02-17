import pytest
from sqlalchemy.orm import Session

from src.toki_pona_api.crud.group import crud_group
from src.toki_pona_api.schemas.group import GroupCreate, GroupBase
from src.toki_pona_api.models.group import Group
from src.toki_pona_api.models.word import Word

def test_create_group(db_session):
    """Test creating a new group."""
    group_data = GroupCreate(
        name="test_group",
        description="A test group"
    )
    group = crud_group.create(db_session, obj_in=group_data)
    assert group.name == "test_group"
    assert group.description == "A test group"
    assert len(group.words) == 0

def test_get_group_by_name(db_session, sample_group):
    """Test retrieving a group by name."""
    group = crud_group.get_by_name(db_session, name="Basic Words")
    assert group is not None
    assert group.id == sample_group
    assert group.description == "Essential Toki Pona vocabulary"

def test_add_word_to_group(db_session, sample_group, sample_words):
    """Test adding a word to an existing group."""
    group = crud_group.get(db_session, id=sample_group)
    initial_word_count = len(group.words)
    
    # Create a new word to add
    new_word = Word(
        toki_pona="ilo",
        english="tool",
        definition="tool, device, machine, implement",
        components={"root": "ilo"}
    )
    db_session.add(new_word)
    db_session.flush()
    
    # Add new word to group
    updated_group = crud_group.add_word(db_session, group_id=sample_group, word_id=new_word.id)
    
    # Verify word was added
    assert len(updated_group.words) == initial_word_count + 1
    assert any(word.toki_pona == "ilo" for word in updated_group.words)

def test_get_multi_groups(db_session, sample_group):
    """Test retrieving multiple groups with pagination."""
    # Create additional groups
    additional_groups = [
        GroupCreate(name=f"test_group_{i}", description=f"Description {i}")
        for i in range(2)  # Create 2 more groups
    ]
    for group_data in additional_groups:
        crud_group.create(db_session, obj_in=group_data)
    
    # Get all groups and verify words relationship is loaded
    groups = crud_group.get_multi(db_session, skip=0, limit=10)
    assert len(groups) == 3  # sample_group + 2 new groups
    assert all(hasattr(g, 'words') for g in groups)  # Check words relationship is loaded
    
    # Test pagination
    groups_page = crud_group.get_multi(db_session, skip=1, limit=2)
    assert len(groups_page) == 2