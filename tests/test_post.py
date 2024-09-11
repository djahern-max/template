import pytest
from app import models

def test_get_all_posts(client, test_user, test_posts):
    response = client.post("/auth/login", data={"username": test_user['username'], "password": test_user['password']})  # Updated
    assert response.status_code == 200
    token = response.json()["access_token"]
    
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.get("/posts/", headers=headers)
    assert response.status_code == 200

    posts = response.json()
    assert len(posts) == len(test_posts)  

    titles = [post["title"] for post in posts]
    contents = [post["content"] for post in posts]

    for post in test_posts:
        assert post.title in titles
        assert post.content in contents

def test_unauthorized_user_cannot_get_posts(client):
    response = client.get("/posts/")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_get_post_by_id(client, test_user, test_posts):
    response = client.post("/auth/login", data={"username": test_user['username'], "password": test_user['password']})  # Updated
    assert response.status_code == 200
    token = response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    post_id = test_posts[0].id
    response = client.get(f"/posts/{post_id}", headers=headers)
    assert response.status_code == 200

    post = response.json()
    assert post["title"] == test_posts[0].title
    assert post["content"] == test_posts[0].content
    assert post["id"] == test_posts[0].id

def test_unauthorized_user_cannot_get_non_existent_post(client):
    response = client.get("/posts/8888")  
    assert response.status_code == 404  

@pytest.mark.parametrize("title, content, published", [
    ("Test Post", "This is a test post", True),
    ("Another Post", "This is another test post", False),
])
def test_create_post(client, test_user, title, content, published):
    # Login to get the token
    response = client.post("/auth/login", data={"username": test_user['username'], "password": test_user['password']})  # Updated
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Dynamically create post_data based on the parameters
    post_data = {
        "title": title,
        "content": content,
        "published": published
    }

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Create the post
    response = client.post("/posts/", json=post_data, headers=headers)
    assert response.status_code == 201

    # Check the created post
    created_post = response.json()
    assert created_post["title"] == post_data["title"]
    assert created_post["content"] == post_data["content"]
    assert created_post["published"] == post_data["published"]
    print(response.json())

def test_create_post_default_published_true(client, test_user, test_posts):
    response = client.post("/auth/login", data={"username": test_user['username'], "password": test_user['password']})  # Updated
    assert response.status_code == 200
    token = response.json()["access_token"]

    post_data = {
        "title": "Test Post",
        "content": "This is a test post",
    }

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.post("/posts/", json=post_data, headers=headers)
    assert response.status_code == 201

    created_post = response.json()
    assert created_post["title"] == post_data["title"]
    assert created_post["content"] == post_data["content"]
    assert created_post["published"] == True
    print(response.json())

def test_unauthorized_user_create_post(client):
    post_data = {
        "title": "Test Post",
        "content": "This is a test post",
    }

    response = client.post("/posts/", json=post_data)
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_unauthorized_user_cannot_delete_post(client, test_posts):
    # Try to delete a post without authorization (using a real post ID)
    post_id = test_posts[0].id
    response = client.delete(f"/posts/{post_id}")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_delete_post(client, test_user, test_posts):
    # Login to get the token
    response = client.post("/auth/login", data={"username": test_user['username'], "password": test_user['password']})  # Updated
    assert response.status_code == 200
    token = response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Get the post ID from the first test post
    post_id = test_posts[0].id

    # Delete the post
    response = client.delete(f"/posts/{post_id}", headers=headers)
    assert response.status_code == 200

    # Verify that the post is actually deleted by trying to get it
    response = client.get(f"/posts/{post_id}", headers=headers)
    assert response.status_code == 404

def test_user_cannot_delete_another_users_post(client, test_user, test_posts, session):
    # Ensure test_posts are created properly
    assert len(test_posts) > 0, "No posts were created in the fixture"

    # Create a second user who will attempt to delete the first user's post
    second_user_data = {
        "username": "seconduser",  # Updated
        "password": "password123"
    }
    response = client.post("/users/", json=second_user_data)
    assert response.status_code == 200

    # Login with the second user
    response = client.post("/auth/login", data={"username": second_user_data['username'], "password": second_user_data['password']})  # Updated
    assert response.status_code == 200
    token = response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Re-query the post created by the first user to ensure it's bound to the current session
    post = session.query(models.Post).filter(models.Post.user_id == test_user['id']).first()
    assert post is not None, "The post was not found in the database"

    post_id = post.id

    # Attempt to delete the post created by the first test_user
    response = client.delete(f"/posts/{post_id}", headers=headers)

    # Expecting 403 Forbidden because the post belongs to another user
    assert response.status_code == 403
    assert response.json() == {"detail": "You are not authorized to delete this post"}

def test_update_post(client, test_user, test_posts):
    # Login to get the token
    response = client.post("/auth/login", data={"username": test_user['username'], "password": test_user['password']})  # Updated
    assert response.status_code == 200
    token = response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Get the post ID from the first test post
    post_id = test_posts[0].id

    # Data to update the post with
    updated_post_data = {
        "title": "Updated Title",
        "content": "Updated content",
        "published": True
    }

    # Send the update request
    response = client.put(f"/posts/{post_id}", json=updated_post_data, headers=headers)
    assert response.status_code == 200

    # Verify the updated post's content
    updated_post = response.json()
    assert updated_post["title"] == updated_post_data["title"]
    assert updated_post["content"] == updated_post_data["content"]
    assert updated_post["published"] == updated_post_data["published"]

    # Fetch the post again to ensure the changes persisted
    response = client.get(f"/posts/{post_id}", headers=headers)
    assert response.status_code == 200

    post = response.json()
    assert post["title"] == updated_post_data["title"]
    assert post["content"] == updated_post_data["content"]
    assert post["published"] == updated_post_data["published"]

def test_update_non_existent_post(client, test_user):
    # Login to get the token
    response = client.post("/auth/login", data={"username": test_user['username'], "password": test_user['password']})  # Updated
    assert response.status_code == 200
    token = response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Non-existent post ID (e.g., 9999)
    non_existent_post_id = 9999

    # Data to update the post with
    updated_post_data = {
        "title": "Updated Title",
        "content": "Updated content",
        "published": True
    }

    # Try to update a non-existent post
    response = client.put(f"/posts/{non_existent_post_id}", json=updated_post_data, headers=headers)
    
    # Expecting 404 Not Found
    assert response.status_code == 404
    assert response.json() == {"detail": "Post not found"}


