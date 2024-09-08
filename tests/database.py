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
    assert created_post["content"] == post_data["content"]
