# Language Learning Portal - FastAPI Backend

This is the FastAPI backend for the Language Learning Portal, providing RESTful APIs for word management, study groups, and learning sessions.

## Setup

1. Create a Python virtual environment (3.11+ recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Initialize the database:
   ```bash
   python -m alembic upgrade head
   ```

4. Start the development server:
   ```bash
   python -m uvicorn app.main:app --reload
   ```

The API will be available at:
- API Documentation (Swagger UI): http://127.0.0.1:8000/docs
- Alternative Documentation (ReDoc): http://127.0.0.1:8000/redoc
- API Base URL: http://127.0.0.1:8000/api/v1

## Running Tests

From the `backend-fastapi` directory, run:
```bash
pytest -v
```

This will run all tests using an in-memory SQLite database. Add `-s` flag to see print statements and logging output:
```bash
pytest -v -s
```

## API Endpoints

- `/api/v1/words/`: Word management
- `/api/v1/groups/`: Study group management
- `/api/v1/study/`: Study sessions and activities

## Development

- Models are defined in `app/models/`
- API routes are in `app/api/api_v1/endpoints/`
- Database migrations are managed with Alembic
- Configuration settings are in `app/core/config.py`
