import pytest
from app import models

def test_vote_on_post(client, test_user, test_posts):
    response = client.post("/auth/login", data={"username": test_user['username'], "password": test_user['password']})  # Updated
    assert response.status_code == 200
    token = response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    vote_data = {
        "post_id": test_posts[0].id,
        "dir": 1 
    }

    response = client.post("/vote/", json=vote_data, headers=headers)
    assert response.status_code == 201
    assert response.json() == {"message": "Vote recorded successfully"}

def test_remove_vote_on_post(client, test_user, test_posts):
    response = client.post("/auth/login", data={"username": test_user['username'], "password": test_user['password']})  # Updated
    assert response.status_code == 200
    token = response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    vote_data = {
        "post_id": test_posts[0].id,
        "dir": 1  
    }
    response = client.post("/vote/", json=vote_data, headers=headers)
    assert response.status_code == 201
    vote_data["dir"] = 0  
    response = client.post("/vote/", json=vote_data, headers=headers)
    assert response.status_code == 201
    assert response.json() == {"message": "Vote deleted successfully"}

def test_vote_on_non_existent_post(client, test_user):
    response = client.post("/auth/login", data={"username": test_user['username'], "password": test_user['password']})  # Updated
    assert response.status_code == 200
    token = response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    vote_data = {
        "post_id": 9999,  
        "dir": 1  
    }
    response = client.post("/vote/", json=vote_data, headers=headers)
    assert response.status_code == 404
    assert response.json() == {"detail": "Post with id 9999 does not exist"}

def test_duplicate_vote(client, test_user, test_posts):
    response = client.post("/auth/login", data={"username": test_user['username'], "password": test_user['password']})  # Updated
    assert response.status_code == 200
    token = response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    vote_data = {
        "post_id": test_posts[0].id,
        "dir": 1
    }
    response = client.post("/vote/", json=vote_data, headers=headers)
    assert response.status_code == 201

    response = client.post("/vote/", json=vote_data, headers=headers)
    assert response.status_code == 409
    assert response.json() == {"detail": f"User {test_user['id']} has already voted on post {test_posts[0].id}"}
