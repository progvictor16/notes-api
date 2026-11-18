from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select

from database import create_db_and_tables, get_session
from models import Note, NoteCreate

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()


def find_note(note_id: int, session: Session):
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/notes")
def create_note(note: NoteCreate, session: SessionDep):
    new_note = Note(title=note.title, content=note.content)
    session.add(new_note)
    session.commit()
    session.refresh(new_note)
    return new_note


@app.get("/notes")
def get_notes(session: SessionDep):
    return session.exec(select(Note)).all()


@app.get("/notes/{note_id}")
def get_note(note_id: int, session: SessionDep):
    note = find_note(note_id, session)
    return note


@app.put("/notes/{note_id}")
def modify_note(note_id: int, updated_note: NoteCreate, session: SessionDep):
    note = find_note(note_id, session)
    note.title = updated_note.title
    note.content = updated_note.content
    session.add(note)
    session.commit()
    session.refresh(note)
    return note


@app.delete("/notes/{note_id}")
def delete_note(note_id: int, session: SessionDep):
    note = find_note(note_id, session)
    session.delete(note)
    session.commit()
    return note
