"""
Common dependencies for FastAPI endpoints.
"""
from .db.session import get_db

__all__ = ["get_db"]

# Add more dependencies as needed, such as:
# - Authentication
# - Rate limiting
# - Caching
