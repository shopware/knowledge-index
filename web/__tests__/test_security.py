from fastapi.testclient import TestClient
from ..main import app
import os

client = TestClient(app)


def test_require_api_key():
    response = client.get('/me')
    print(response)

    assert response.status_code == 403
    assert response.json() == {"detail": "Not authenticated"}


def test_require_api_key_wrong():
    os.environ['KNOWLEDGE_API_KEY'] = 'testapikey'
    response = client.get('/me', headers={"X-Shopware-Api-Key": "wrongapikey"})

    assert response.status_code == 403
    assert response.json() == {"detail": "Could not validate API KEY"}

    os.environ.pop('KNOWLEDGE_API_KEY')


def test_require_api_key_ok():
    os.environ['KNOWLEDGE_API_KEY'] = 'correctapikey'
    response = client.get('/me', headers={"X-Shopware-Api-Key": "correctapikey"})

    assert response.status_code == 200

    os.environ.pop('KNOWLEDGE_API_KEY')
