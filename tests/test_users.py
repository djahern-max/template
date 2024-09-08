from app import schemas
from .database import client, session
from app.config import settings
import jwt

def test_root(client):
    res = client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') == "Welcome to ryze!"
    assert res.status_code == 200

# Test for creating user
def test_create_user(client):
    res = client.post("/users/", json={"email": "test@gmail.com", "password": "123456"})
    new_user = schemas.UserOut(**res.json())
    print(res.json())
    assert new_user.email == "test@gmail.com"
    assert res.status_code == 200

def test_login_user(client):
    res = client.post(
        "/auth/login", data={"username": "test@gmail.com", "password": "123456"})
    print(res.json())
    assert res.status_code == 200


