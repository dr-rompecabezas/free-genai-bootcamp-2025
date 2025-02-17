from src.toki_pona_api.crud import crud_word
from src.toki_pona_api.models import Word
from src.toki_pona_api.api.v1.utils import SortOrder

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
    # Get words for the group with default sorting
    group_words = crud_word.get_by_group(db_session, group_id=sample_group)
    assert len(group_words) == 2
    assert group_words[0].toki_pona == "pona"  # Alphabetically first
    assert group_words[1].toki_pona == "telo"  # Alphabetically second
    
    # Test pagination
    paginated_words = crud_word.get_by_group(db_session, group_id=sample_group, skip=1, limit=1)
    assert len(paginated_words) == 1
    assert paginated_words[0].toki_pona == "telo"  # Second word
    
    # Test sorting by english
    sorted_by_english = crud_word.get_by_group(
        db_session,
        group_id=sample_group,
        sort_by="english"
    )
    assert len(sorted_by_english) == 2
    assert sorted_by_english[0].english == "good"  # "pona"
    assert sorted_by_english[1].english == "water"  # "telo"
    
    # Test descending order
    sorted_desc = crud_word.get_by_group(
        db_session,
        group_id=sample_group,
        sort_by="toki_pona",
        order=SortOrder.DESC
    )
    assert len(sorted_desc) == 2
    assert sorted_desc[0].toki_pona == "telo"  # Alphabetically higher
    assert sorted_desc[1].toki_pona == "pona"  # Alphabetically lower
    
    # Test with non-existent group
    non_existent_group_words = crud_word.get_by_group(db_session, group_id=99999)
    assert len(non_existent_group_words) == 0

def test_get_multi(db_session, sample_words):
    """Test retrieving multiple words with sorting and pagination."""
    # Test default sorting
    words = crud_word.get_multi(db_session)
    assert len(words) == 2
    assert words[0].toki_pona == "pona"  # Alphabetically first
    assert words[1].toki_pona == "telo"  # Alphabetically second
    
    # Test pagination
    paginated_words = crud_word.get_multi(db_session, skip=1, limit=1)
    assert len(paginated_words) == 1
    assert paginated_words[0].toki_pona == "telo"  # Second word
    
    # Test sorting by english
    sorted_by_english = crud_word.get_multi(
        db_session,
        sort_by="english"
    )
    assert len(sorted_by_english) == 2
    assert sorted_by_english[0].english == "good"  # "pona"
    assert sorted_by_english[1].english == "water"  # "telo"
    
    # Test descending order
    sorted_desc = crud_word.get_multi(
        db_session,
        sort_by="toki_pona",
        order=SortOrder.DESC
    )
    assert len(sorted_desc) == 2
    assert sorted_desc[0].toki_pona == "telo"  # Alphabetically higher
    assert sorted_desc[1].toki_pona == "pona"  # Alphabetically lower

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
