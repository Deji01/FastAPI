from starlette.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_ping():
    respose = client.get("/ping")
    assert response.status == 200
    assert response.json() == {"ping": "pong!"}