import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import models, schemas
from app.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Use SQLite for testing
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency to use the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create test client
client = TestClient(app)

@pytest.fixture(scope="function", autouse=True)
def setup_database():
    # Drop all tables and recreate them for each test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_post():
    # First, create a user and login to get the token
    response = client.post("/users/", json={"email": "testuser@example.com", "password": "password123"})
    assert response.status_code == 200 or response.status_code == 201  # Accept both 200 and 201
    user_data = response.json()

    response = client.post("/auth/login", data={"username": "testuser@example.com", "password": "password123"})
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Use the token to create a post
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
