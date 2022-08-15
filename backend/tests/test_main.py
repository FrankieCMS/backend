import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


class TestMainRoutes:
    @pytest.mark.asyncio
    async def test_read_main(self, app: FastAPI, client: TestClient):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"Hello": "Mundo!"}
