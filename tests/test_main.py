from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the FastAPI Calculator!"}


def test_add():
    response = client.post("/add", json={"a": 5, "b": 3})
    assert response.status_code == 200
    assert response.json()["result"] == 8
    assert response.json()["operation"] == "add"


def test_subtract():
    response = client.post("/subtract", json={"a": 10, "b": 4})
    assert response.status_code == 200
    assert response.json()["result"] == 6
    assert response.json()["operation"] == "subtract"


def test_multiply():
    response = client.post("/multiply", json={"a": 7, "b": 6})
    assert response.status_code == 200
    assert response.json()["result"] == 42
    assert response.json()["operation"] == "multiply"


def test_divide_normal():
    response = client.post("/divide", json={"a": 20, "b": 5})
    assert response.status_code == 200
    assert response.json()["result"] == 4
    assert response.json()["operation"] == "divide"


def test_divide_by_zero():
    response = client.post("/divide", json={"a": 20, "b": 0})
    assert response.status_code == 400
    assert response.json()["detail"] == "Cannot divide by zero!"


def test_power():
    response = client.post("/power", json={"a": 2, "b": 3})
    assert response.status_code == 200
    assert response.json()["result"] == 8
    assert response.json()["operation"] == "power"


def test_modulus_normal():
    response = client.post("/modulus", json={"a": 10, "b": 3})
    assert response.status_code == 200
    assert response.json()["result"] == 1
    assert response.json()["operation"] == "modulus"


def test_modulus_by_zero():
    response = client.post("/modulus", json={"a": 10, "b": 0})
    assert response.status_code == 400
    assert response.json()["detail"] == "Cannot modulo by zero!"


def test_floor_divide_normal():
    response = client.post("/floor_divide", json={"a": 20, "b": 3})
    assert response.status_code == 200
    assert response.json()["result"] == 6
    assert response.json()["operation"] == "floor_divide"


def test_floor_divide_by_zero():
    response = client.post("/floor_divide", json={"a": 20, "b": 0})
    assert response.status_code == 400
    assert response.json()["detail"] == "Cannot divide by zero!"


def test_history_length():
    client.post("/add", json={"a": 1, "b": 1})
    client.post("/subtract", json={"a": 2, "b": 1})
    client.post("/multiply", json={"a": 2, "b": 2})
    
    response = client.get("/history")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3
    for entry in data:
        assert "operation" in entry
        assert "a" in entry
        assert "b" in entry
        assert "result" in entry
