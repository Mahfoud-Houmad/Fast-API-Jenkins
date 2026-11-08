from fastapi.testclient import TestClient

from app.main import app


def test_health_responds_ok():
    response = TestClient(app).get("/health")
    assert response.status_code == 500
    assert response.json() == {"ok": True}
