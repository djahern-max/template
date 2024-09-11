import pytest
from jose import jwt
from app import schemas
from app.config import settings


def test_create_user(client):
    res = client.post("/users/", json={"username": "testuser", "password": "123456"})  
    new_user = schemas.UserOut(**res.json()).model_dump()
    assert new_user['username'] == "testuser" 



def test_login_user(client, test_user):
    res = client.post(
        "/auth/login", data={"username": test_user['username'], "password": test_user['password']}) 
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, settings.algorithm)
    id = int(payload.get('sub'))  
    assert id == test_user['id']



@pytest.mark.parametrize("username, password, status_code", [
    ('wrongusername', '123456', 401),  
    ('testuser', 'wrongpassword', 401), 
    ('wrongusername', 'wrongpassword', 401),  
    (None, '123456', 401), 
    ('testuser', None, 401)  
])
def test_incorrect_login(client, test_user, username, password, status_code):
    res = client.post(
        "/auth/login", data={"username": username, "password": password}) 
    assert res.status_code == status_code







