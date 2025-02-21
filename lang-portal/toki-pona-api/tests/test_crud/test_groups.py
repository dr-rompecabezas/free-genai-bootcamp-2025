import pytest
from sqlalchemy.orm.exc import FlushError

from src.toki_pona_api.crud.group import crud_group
from src.toki_pona_api.schemas.group import GroupCreate
from src.toki_pona_api.models.word import Word
from src.toki_pona_api.api.v1.utils import SortOrder

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
    # Test with existing group
    group = crud_group.get_by_name(db_session, name="Basic Words")
    assert group is not None
    assert group.id == sample_group
    assert group.description == "Essential Toki Pona vocabulary"
    
    # Test with non-existent group
    non_existent_group = crud_group.get_by_name(db_session, name="NonExistentGroup")
    assert non_existent_group is None

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
    
    # Test with non-existent group
    with pytest.raises(AttributeError):
        crud_group.add_word(db_session, group_id=99999, word_id=new_word.id)
    
    # Test with non-existent word
    with pytest.raises(FlushError):
        crud_group.add_word(db_session, group_id=sample_group, word_id=99999)

def test_remove_word_from_group(db_session, sample_group, sample_words):
    """Test removing a word from a group."""
    group = crud_group.get(db_session, id=sample_group)
    initial_word_count = len(group.words)
    word_id = sample_words[0]
    
    # Remove word from group
    updated_group = crud_group.remove_word(db_session, group_id=sample_group, word_id=word_id)
    
    # Verify word was removed
    assert len(updated_group.words) == initial_word_count - 1
    assert not any(word.id == word_id for word in updated_group.words)
    
    # Test with non-existent group
    with pytest.raises(AttributeError):
        crud_group.remove_word(db_session, group_id=99999, word_id=word_id)
    
    # Test with non-existent word
    with pytest.raises(ValueError, match=r"Word with id 99999 not found"):
        crud_group.remove_word(db_session, group_id=sample_group, word_id=99999)
    
    # Test with word not in group
    other_word = Word(
        toki_pona="ilo",
        english="tool",
        definition="tool, device, machine, implement",
        components={"root": "ilo"}
    )
    db_session.add(other_word)
    db_session.flush()
    with pytest.raises(ValueError, match=r"Word with id .* is not in group .*"):
        crud_group.remove_word(db_session, group_id=sample_group, word_id=other_word.id)

def test_get_multi_groups(db_session, sample_group):
    """Test retrieving multiple groups with pagination and sorting."""
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
    
    # Test sorting by name ascending (default)
    sorted_groups = crud_group.get_multi(db_session, sort_by="name")
    assert len(sorted_groups) == 3
    assert sorted_groups[0].name == "Basic Words"  # Alphabetically first
    assert sorted_groups[1].name == "test_group_0"
    assert sorted_groups[2].name == "test_group_1"
    
    # Test sorting by name descending
    sorted_groups_desc = crud_group.get_multi(db_session, sort_by="name", order=SortOrder.DESC)
    assert len(sorted_groups_desc) == 3
    assert sorted_groups_desc[0].name == "test_group_1"
    assert sorted_groups_desc[1].name == "test_group_0"
    assert sorted_groups_desc[2].name == "Basic Words"
    
    # Test with skip > total groups
    empty_groups = crud_group.get_multi(db_session, skip=10, limit=10)
    assert len(empty_groups) == 0