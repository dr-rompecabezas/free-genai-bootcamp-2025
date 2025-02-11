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

4. Seed the database:

   ```bash
   python -m app.db.seed
   ```

5. Start the development server:

   ```bash
   python -m uvicorn app.main:app --reload
   ```

The API will be available at:

- API Documentation (Swagger UI): <http://127.0.0.1:8000/docs>
- Alternative Documentation (ReDoc): <http://127.0.0.1:8000/redoc>
- API Base URL: <http://127.0.0.1:8000/api/v1>

## Database Schema

### Words Schema

- `id`: Primary key
- `kanji`: Japanese word/character (indexed)
- `romaji`: Romanized reading
- `english`: English translation
- `parts`: JSON string containing word components
- `group_id`: Foreign key to Groups table

### Groups Schema

- `id`: Primary key
- `name`: Group name (indexed)
- `description`: Optional group description
- `words_count`: Number of words in the group
- `created_at`: Timestamp of creation

### Study Sessions Schema

- `id`: Primary key
- `group_id`: Foreign key to Groups table
- `started_at`: Session start timestamp
- `completed_at`: Optional session completion timestamp

### Study Activities Schema

- `id`: Primary key
- `session_id`: Foreign key to Study Sessions table
- `word_id`: Foreign key to Words table
- `correct`: Boolean indicating if answer was correct
- `created_at`: Activity timestamp
- `url`: Optional URL for additional resources

## API Endpoints

### Words Endpoints

- `GET /api/v1/words/`: List words with pagination and sorting
- `POST /api/v1/words/`: Create a new word
- `GET /api/v1/words/{word_id}`: Get word details
- `PUT /api/v1/words/{word_id}`: Update word
- `DELETE /api/v1/words/{word_id}`: Delete word

### Groups Endpoints

- `GET /api/v1/groups/`: List all groups
- `POST /api/v1/groups/`: Create a new group
- `GET /api/v1/groups/{group_id}`: Get group details
- `PUT /api/v1/groups/{group_id}`: Update group
- `DELETE /api/v1/groups/{group_id}`: Delete group

### Study Sessions Endpoints

- `GET /api/v1/study/sessions/`: List study sessions
- `POST /api/v1/study/sessions/`: Start a new study session
- `GET /api/v1/study/sessions/{session_id}`: Get session details
- `PUT /api/v1/study/sessions/{session_id}`: Update session (e.g., mark as complete)
- `POST /api/v1/study/activities/`: Record a study activity

## Running Tests

From the `backend-fastapi` directory, run:

```bash
pytest -v
```

This will run all tests using an in-memory SQLite database. Add `-s` flag to see print statements and logging output:

```bash
pytest -v -s
```

## Development

### Project Structure

```text
app/
├── api/                 # API endpoints
│   └── api_v1/
│       └── endpoints/   # API route handlers
├── core/               # Core functionality
│   └── config.py      # Configuration settings
├── db/                # Database
│   ├── base.py       # Base classes
│   └── seed.py       # Database seeding
├── models/            # SQLAlchemy models
├── schemas/           # Pydantic schemas
└── main.py           # Application entry point
```

### Database Migrations

- Migrations are managed with Alembic
- Create a new migration:

  ```bash
  alembic revision --autogenerate -m "description"
  ```

- Apply migrations:

  ```bash
  alembic upgrade head
  ```

- Rollback migration:

  ```bash
  alembic downgrade -1
  ```

### Environment Variables

The following environment variables can be set:

- `DATABASE_URL`: SQLAlchemy database URL (default: SQLite)
- `API_V1_STR`: API version prefix (default: "/api/v1")
- `PROJECT_NAME`: Project name in OpenAPI docs
- `BACKEND_CORS_ORIGINS`: Allowed CORS origins
