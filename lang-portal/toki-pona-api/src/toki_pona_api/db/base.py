from sqlalchemy.orm import DeclarativeBase, registry

# Create the SQLAlchemy declarative base
mapper_registry = registry()

class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    registry = mapper_registry
    metadata = mapper_registry.metadata
