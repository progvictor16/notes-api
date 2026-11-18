# notes-api

A simple REST API for managing notes, built with **FastAPI** and **SQLite**.

## Features

- Full CRUD for notes (create, read, update, delete)
- Data stored in a SQLite database via SQLModel, so notes survive a server restart
- Automatic tests (pytest) running on a separate in-memory database
- Interactive API documentation at `/docs`

## Tech stack

Python 3.10+, FastAPI, SQLModel, SQLite, pytest

## Getting started

```bash
git clone https://github.com/progvictor16/notes-api.git
cd notes-api
python -m venv .venv
```

Activate the virtual environment:

- Windows (PowerShell): `.venv\Scripts\Activate.ps1`
- macOS / Linux: `source .venv/bin/activate`

> If PowerShell blocks the script, run
> `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned` first.

Install dependencies and start the server:

```bash
pip install -r requirements.txt
fastapi dev main.py
```

Open http://127.0.0.1:8000/docs to try the API in your browser.
The database file `notes.db` is created automatically on first start.

## Endpoints

| Method | Path               | Description                          |
|--------|--------------------|--------------------------------------|
| GET    | `/health`          | Check if the server is running       |
| POST   | `/notes`           | Create a note                        |
| GET    | `/notes`           | List all notes                       |
| GET    | `/notes/{note_id}` | Get one note (404 if it doesn't exist) |
| PUT    | `/notes/{note_id}` | Update a note                        |
| DELETE | `/notes/{note_id}` | Delete a note                        |

Example request body for `POST` and `PUT`:

```json
{
  "title": "Shopping",
  "content": "Milk, bread, eggs"
}
```

## Running tests

```bash
python -m pytest
```

Tests use a separate in-memory database, so they never touch `notes.db`.

## Project structure

```
main.py       # API endpoints
models.py     # data models (NoteCreate, Note)
database.py   # database connection and session
test_main.py  # automatic tests
```