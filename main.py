from fastapi import FastAPI, HTTPException

from models import Note, NoteCreate

app = FastAPI()


notes = []
next_id = 1


def find_note(note_id: int):
    for note in notes:
        if note.id == note_id:
            return note
    raise HTTPException(status_code=404, detail="Note not found")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/notes")
def create_note(note: NoteCreate):
    global next_id
    new_note = Note(id=next_id, title=note.title, content=note.content)
    next_id += 1
    notes.append(new_note)
    return new_note


@app.get("/notes")
def get_notes():
    return notes


@app.get("/notes/{note_id}")
def get_note(note_id: int):
    note = find_note(note_id)
    return note


@app.put("/notes/{note_id}")
def modify_note(note_id: int, updated_note: NoteCreate):
    note = find_note(note_id)
    note.title = updated_note.title
    note.content = updated_note.content
    return note


@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    note = find_note(note_id)
    notes.remove(note)
    return note
