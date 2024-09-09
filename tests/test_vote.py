import pytest
from app import models

def test_vote_on_post(client, test_user, test_posts):
    # Login to get the token
    response = client.post("/auth/login", data={"username": test_user['email'], "password": test_user['password']})
    assert response.status_code == 200
    token = response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Vote on a post (upvote)
    vote_data = {
        "post_id": test_posts[0].id,
        "dir": 1  # Upvote
    }

    response = client.post("/vote/", json=vote_data, headers=headers)
    assert response.status_code == 201
    assert response.json() == {"message": "Vote recorded successfully"}

def test_remove_vote_on_post(client, test_user, test_posts):
    # Login to get the token
    response = client.post("/auth/login", data={"username": test_user['email'], "password": test_user['password']})
    assert response.status_code == 200
    token = response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Upvote a post first
    vote_data = {
        "post_id": test_posts[0].id,
        "dir": 1  # Upvote
    }
    response = client.post("/vote/", json=vote_data, headers=headers)
    assert response.status_code == 201

    # Remove the vote (downvote)
    vote_data["dir"] = 0  # Remove vote
    response = client.post("/vote/", json=vote_data, headers=headers)
    assert response.status_code == 201
    assert response.json() == {"message": "Vote deleted successfully"}

def test_vote_on_non_existent_post(client, test_user):
    # Login to get the token
    response = client.post("/auth/login", data={"username": test_user['email'], "password": test_user['password']})
    assert response.status_code == 200
    token = response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Attempt to vote on a non-existent post
    vote_data = {
        "post_id": 9999,  # Non-existent post
        "dir": 1  # Upvote
    }
    response = client.post("/vote/", json=vote_data, headers=headers)
    assert response.status_code == 404
    assert response.json() == {"detail": "Post with id 9999 does not exist"}

def test_duplicate_vote(client, test_user, test_posts):
    # Login to get the token
    response = client.post("/auth/login", data={"username": test_user['email'], "password": test_user['password']})
    assert response.status_code == 200
    token = response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Upvote a post
    vote_data = {
        "post_id": test_posts[0].id,
        "dir": 1  # Upvote
    }
    response = client.post("/vote/", json=vote_data, headers=headers)
    assert response.status_code == 201

    # Try to upvote again (should return 409 Conflict)
    response = client.post("/vote/", json=vote_data, headers=headers)
    assert response.status_code == 409
    assert response.json() == {"detail": f"User {test_user['id']} has already voted on post {test_posts[0].id}"}
