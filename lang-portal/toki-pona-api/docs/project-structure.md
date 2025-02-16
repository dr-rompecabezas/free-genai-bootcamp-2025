# Project Structure

1. Project Root:

    - `requirements.txt`: Project dependencies
    - `pyproject.toml`: Modern Python project metadata
    - `.env.example`: Environment variables
    - `alembic.ini`: Database migration configuration

2. Source Code (`src/toki_pona_api/`):

    - `main.py`: Application entry point
    - `config.py`: Configuration management
    - `dependencies.py`: FastAPI dependencies
    - `exceptions.py`: Custom exception classes

3. API Structure (`api/`):

    - Version-controlled API (`v1/`)
    - Separate endpoint modules for each resource
    - Central router combining all endpoints

4. Data Layer:

    - `crud/`: CRUD operations for each model
    - `models/`: SQLAlchemy models
    - `schemas/`: Pydantic models for request/response
    - `db/`: Database configuration and session management

5. Tests:

    - Separate test directories for API and CRUD operations
    - `conftest.py` for pytest fixtures
    - Parallel structure to source code

6. Migrations:

    - Alembic migrations for database schema changes

```plaintext
toki-pona-api/
├── README.md
├── requirements.txt
├── .env
├── .gitignore
├── alembic.ini                 # Alembic migrations config
├── pyproject.toml              # Project metadata and dependencies
├── src/
│   └── toki_pona_api/
│       ├── __init__.py
│       ├── main.py             # FastAPI app initialization
│       ├── config.py           # Configuration management
│       ├── dependencies.py     # FastAPI dependencies
│       ├── exceptions.py       # Custom exceptions
│       ├── constants.py        # Constants and enums
│       ├── api/
│       │   ├── __init__.py
│       │   ├── v1/
│       │   │   ├── __init__.py
│       │   │   ├── router.py   # API router combining all routes
│       │   │   ├── endpoints/
│       │   │   │   ├── __init__.py
│       │   │   │   ├── words.py
│       │   │   │   ├── groups.py
│       │   │   │   └── study_sessions.py
│       ├── crud/
│       │   ├── __init__.py
│       │   ├── base.py        # Base CRUD class
│       │   ├── words.py
│       │   ├── groups.py
│       │   └── study_sessions.py
│       ├── db/
│       │   ├── __init__.py
│       │   ├── session.py     # Database session management
│       │   └── base.py        # SQLAlchemy base class
│       ├── models/            # SQLAlchemy models
│       │   ├── __init__.py
│       │   ├── word.py
│       │   ├── group.py
│       │   └── study_session.py
│       └── schemas/           # Pydantic models
│           ├── __init__.py
│           ├── word.py
│           ├── group.py
│           └── study_session.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # pytest configuration
│   ├── test_api/
│   │   ├── __init__.py
│   │   ├── test_words.py
│   │   ├── test_groups.py
│   │   └── test_study_sessions.py
│   └── test_crud/
│       ├── __init__.py
│       ├── test_words.py
│       ├── test_groups.py
│       └── test_study_sessions.py
└── migrations/               # Alembic migrations
    ├── env.py
    ├── script.py.mako
    └── versions/
```
