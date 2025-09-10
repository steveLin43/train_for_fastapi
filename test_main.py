from fastapi.testclient import TestClient
from typing import Annotated, Union
from main import app

client = TestClient(app)
# 略過身分認證
async def override_dependency(q: Union[str, None] = None):
    return {"q": q, "skip": 5, "limit": 10}
app.dependency_overrides[common_parameters] = override_dependency

def test_read_main():
    response = client.get("/read_main")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": None, "skip": 5, "limit": 10},
    }

def test_read_items():
    with TestClient(app) as client:
        response = client.get("/items/foo")
        assert response.status_code == 200
        assert response.json() == {"name": "Fighters"}