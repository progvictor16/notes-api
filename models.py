from sqlmodel import Field, SQLModel


class NoteCreate(SQLModel):
    title: str
    content: str


class Note(NoteCreate, table=True):
    id: int | None = Field(default=None, primary_key=True)
