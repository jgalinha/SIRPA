from api import __version__
from api.main import app
from fastapi import status
from fastapi.testclient import TestClient

client = TestClient(app)


def test_version():
    assert __version__ == "0.1.0"


def test_index():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"SIRPA API": "Visit docs for more information"}
