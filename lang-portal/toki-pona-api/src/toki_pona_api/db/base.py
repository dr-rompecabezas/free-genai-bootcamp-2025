from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import registry

# Create the SQLAlchemy declarative base
mapper_registry = registry()
Base = declarative_base(metadata=mapper_registry.metadata)
