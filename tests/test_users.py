from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    res = client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') == "Welcome to ryze!"
    assert res.status_code == 200

def test_create_user():


    res = client.post("/users/", json={"email": "test@gmail.com", "password": "123456"})
    assert res.status_code == 200
    print(res.json())