import pytest
from starlette.testclient import TestClient

from app import app


class MongoCustomMock:
    db = []

    async def find_one(self, data: dict) -> dict:
        filtered = [
            item for item in self.db if item.get(
                "appointment_id"
            ) == data.get("appointment_id")
        ]
        return filtered and filtered.pop() or {}
    
    async def create(self, data:dict) -> dict:
        self.db.append(data)
        return data


@pytest.fixture(scope="module")
def test_app():
    app.db = {
        "invoice": MongoCustomMock()
    }
    client = TestClient(app)
    yield client
