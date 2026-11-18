import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from database import get_session
from main import app


@pytest.fixture(name="client")
def client_fixture():
    # 1. baza w pamięci RAM ("sqlite://" bez nazwy pliku = w pamięci)
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    # 2. utwórz tabele w tej pustej bazie
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        # 3. podmień get_session na sesję testową
        def get_session_override():
            return session

        app.dependency_overrides[get_session] = get_session_override

        # 4. daj testowi klienta
        yield TestClient(app)

        # 5. po teście: cofnij podmianę
        app.dependency_overrides.clear()


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_note(client):
    response = client.post("/notes", json={"title": "title", "content": "content"})
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["title"] == "title"
    assert response.json()["content"] == "content"


def test_get_note(client):
    response = client.post("/notes", json={"title": "Zakupy", "content": "content"})
    note_id = response.json()["id"]

    response = client.get(f"/notes/{note_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Zakupy"


def test_get_note_not_found(client):
    response = client.get("/notes/9999")
    assert response.status_code == 404


def test_update_note(client):
    response = client.post("/notes", json={"title": "title", "content": "content"})
    assert response.status_code == 200
    note_id = response.json()["id"]

    response = client.put(
        f"/notes/{note_id}", json={"title": "title1", "content": "content1"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "title1"
    assert response.json()["content"] == "content1"


def test_delete_note(client):
    response = client.post("/notes", json={"title": "title", "content": "content"})
    assert response.status_code == 200
    note_id = response.json()["id"]

    response = client.delete(f"/notes/{note_id}")
    assert response.status_code == 200

    response = client.get(f"/notes/{note_id}")
    assert response.status_code == 404


def test_invalid_id(client):
    response = client.get("/notes/abc")
    assert response.status_code == 422