import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_upload_invalid_file():
    response = client.post(
        "/api/v1/resume/upload",
        files={"file": ("test.txt", b"plain text", "text/plain")},
    )
    assert response.status_code == 400

def test_get_nonexistent_session():
    response = client.get("/api/v1/session/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404