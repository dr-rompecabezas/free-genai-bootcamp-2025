# Toki Pona API

[![Test](https://github.com/dr-rompecabezas/free-genai-bootcamp-2025/actions/workflows/backend_tests.yml/badge.svg)](https://github.com/dr-rompecabezas/free-genai-bootcamp-2025/actions/workflows/backend_tests.yml)
[![codecov](https://codecov.io/gh/dr-rompecabezas/free-genai-bootcamp-2025/branch/main/graph/badge.svg?token=your-codecov-token)](https://codecov.io/gh/dr-rompecabezas/free-genai-bootcamp-2025)

A FastAPI-based REST API for managing Toki Pona language learning resources.

## Features

- CRUD operations for Toki Pona words and word groups
- Study session tracking with word reviews
- SQLAlchemy 2.0 with async support
- 100% test coverage
- OpenAPI documentation

## Development Setup

1. Create a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

2. Install dependencies:

    ```bash
    pip install -e ".[test]"
    ```

3. Set up environment variables:

    ```bash
    cp .env.example .env
    # Edit .env with your configuration
    ```

4. Run migrations:

    ```bash
    alembic upgrade head
    ```

5. Start the server:

    ```bash
    uvicorn src.toki_pona_api.main:app --reload
    ```

## Running Tests

Run tests with coverage:

```bash
pytest --cov=src --cov-report=term-missing
```

## Project Structure

The project follows a modular structure with clear separation of concerns:

- `api/`: API routes and endpoints
- `crud/`: Database CRUD operations
- `models/`: SQLAlchemy models
- `schemas/`: Pydantic models
- `db/`: Database configuration and session management
- `tests/`: Test suite with 100% coverage
