import pytest

from datetime import datetime

from starlette.testclient import TestClient

from app import app


class Obj():
    pass


class MongoCustomMock:
    db = []

    async def find_one(self, data: dict) -> dict:
        filtered = [
            item for item in self.db if item.get("id") in [
                data.get("id"), data.get("_id")
            ]
        ]
        return filtered and filtered.pop() or {}
    
    async def insert_one(self, data: dict) -> dict:
        self.db.append(data)
        obj = Obj()
        obj.inserted_id = data.get("id")
        return obj

    async def update_one(self, query: dict, data: dict) -> dict:
        obj = Obj()
        obj.matched_count = 0
        for item in self.db:
            if item.get("id") == query.get("id"):
                item['end_date'] = datetime.now()
                obj.matched_count += 1
        return obj


@pytest.fixture(scope="module")
def test_app():
    app.db = {
        "appointment": MongoCustomMock()
    }
    client = TestClient(app)
    yield client
