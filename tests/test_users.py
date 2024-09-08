from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app import schemas, models  # models import needed
from app.database import get_db

# Database URL
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Guitar0123!@localhost:5432/fastapi_test'

def test_root(client):
    res = client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') == "Welcome to ryze!"
    assert res.status_code == 200


# Create engine and session
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def session():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create client fixture
@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

# Test for creating user
def test_create_user(client):
    res = client.post("/users/", json={"email": "test@gmail.com", "password": "123456"})
    new_user = schemas.UserOut(**res.json())
    print(res.json())
    assert new_user.email == "test@gmail.com"
    assert res.status_code == 200

