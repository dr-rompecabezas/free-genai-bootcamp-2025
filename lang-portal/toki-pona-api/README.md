# Toki Pona API

A FastAPI-based REST API for managing Toki Pona language learning resources.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
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

## Project Structure

The project follows a modular structure with clear separation of concerns:
- `api/`: API routes and endpoints
- `crud/`: Database CRUD operations
- `db/`: Database configuration and session management
- `models/`: SQLAlchemy models
- `schemas/`: Pydantic models for request/response validation
