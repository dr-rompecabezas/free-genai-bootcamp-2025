# Project Structure

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
