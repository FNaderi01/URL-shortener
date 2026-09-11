# FastAPI URL Shortener

A small URL shortener project built to get familiar with FastAPI.

The app lets you create a short URL, redirect through it, view admin info, and delete/deactivate a shortened URL.

## Learning Phases

This project was implemented in two simple phases:

1. **Sync SQLite version**
   - Used SQLite for local storage.
   - Used regular synchronous SQLAlchemy sessions.
   - Focused on learning basic FastAPI routing, schemas, and CRUD structure.

2. **Async PostgreSQL version**
   - Switched the database connection to PostgreSQL using `asyncpg`.
   - Updated the database layer and routes to use `async` / `await`.
   - Used FastAPI's async support more directly.

## Tech Stack

- FastAPI
- SQLAlchemy
- PostgreSQL
- asyncpg
- Pydantic
- Uvicorn

## Setup

Install dependencies:

```powershell
pip install -r requirements.txt
```

Create a `.env` file with your local settings:

```env
ENV_NAME="Development"
BASE_URL="http://127.0.0.1:8000"
DB_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/shortener"
```

Make sure PostgreSQL is running and the `shortener` database exists.

## Run

```powershell
venv\Scripts\python.exe -m uvicorn shortener_app.main:app --reload
```

The app runs at:

```text
http://127.0.0.1:8000
```

## Basic API Test

Create a short URL:

```powershell
Invoke-RestMethod -Method Post `
  -Uri http://127.0.0.1:8000/url `
  -ContentType "application/json" `
  -Body '{"target_url":"https://example.com"}'
```

Use the returned `url` to test the redirect, and the returned `admin_url` to view or delete the short URL.

## Notes

This is intentionally a small learning project, not a production-ready URL shortener. For a real app, migrations, stronger validation, better error handling, and tests would be added.
