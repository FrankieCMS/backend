from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_regiater_user():
    response = client.post(
        "/v1/users/register",
        json={
            "name": "Francisco Barrento",
            "username": "fbarrento",
            "email": "francisco.barrento@gmail.com",
            "password": "string",
        },
    )

    assert response.status_code == 200
