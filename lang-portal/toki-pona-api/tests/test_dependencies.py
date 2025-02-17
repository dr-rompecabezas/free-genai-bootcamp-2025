import pytest
from sqlalchemy.orm import Session

from toki_pona_api.db.session import get_db


def test_get_db():
    """Test that get_db yields a database session and closes it properly"""
    # Get the session from the generator
    db_gen = get_db()
    db = next(db_gen)
    
    # Verify we got a valid session
    assert isinstance(db, Session)
    
    # Verify we can use the session
    assert db.bind is not None
    
    # Simulate FastAPI's dependency injection cleanup
    try:
        next(db_gen)
    except StopIteration:
        pass
    
    # Verify we can't use the session after cleanup
    with pytest.raises(Exception):
        db.execute("SELECT 1")
