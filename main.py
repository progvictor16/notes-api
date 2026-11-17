from fastapi import FastAPI
from models import Note

app = FastAPI()

notes = []

@app.get("/health")
def health_check():
    return {"status":"ok"}

@app.post("/notes")
def create_note(note: Note):
    notes.append(note)
    return note
    

@app.get("/notes")
def get_notes():
    return notes

