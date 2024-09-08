def test_get_all_posts(client, test_user, test_posts):
    response = client.post("/auth/login", data={"username": test_user['email'], "password": test_user['password']})
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
    response = client.post("/auth/login", data={"username": test_user['email'], "password": test_user['password']})
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



def test_create_post(client, test_user):
    response = client.post("/auth/login", data={"username": test_user['email'], "password": test_user['password']})
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
    print(response.json())   
    assert created_post["content"] == post_data["content"]

