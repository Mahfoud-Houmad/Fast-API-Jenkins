from fastapi.testclient import TestClient

from app.main import app


def test_root_message():
    client = TestClient(app)
    res = client.get("/")
    assert res.status_code == 200
    assert res.json() == {"message": "the server is now active"}


def test_health_ok():
    client = TestClient(app)
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"ok": True}
