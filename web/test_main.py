from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_write_main():
    response = client.post("/")
    assert response.status_code == 405
    assert response.json() == {'detail': 'Method Not Allowed'}

def test_read_healthcheck():
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}