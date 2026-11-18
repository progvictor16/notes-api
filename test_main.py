from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_note():
    response = client.post("/notes", json={"title": "title", "content": "content"})
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["title"] == "title"
    assert response.json()["content"] == "content"


def test_get_note():
    response = client.post("/notes", json={"title": "Zakupy", "content": "content"})
    note_id = response.json()["id"]
    response = client.get(f"/notes/{note_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Zakupy"


def test_get_note_not_found():
    response = client.get("/notes/9999")
    assert response.status_code == 404


def test_update_note():
    response = client.post("/notes", json={"title": "title", "content": "content"})
    assert response.status_code == 200
    note_id = response.json()["id"]
    response = client.put(
        f"/notes/{note_id}", json={"title": "title1", "content": "content1"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "title1"
    assert response.json()["content"] == "content1"


def test_delete_note():
    response = client.post("/notes", json={"title": "title", "content": "content"})
    assert response.status_code == 200
    
    note_id = response.json()["id"]
    
    response = client.delete(f"/notes/{note_id}")
    assert response.status_code == 200
   
    response = client.get(f"/notes/{note_id}")
    assert response.status_code == 404
    
def test_invalid_id():
    response = client.get("/notes/abc")
    assert response.status_code == 422
    