from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app import schemas, models  # models import needed
from app.database import get_db

# Database URL
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Guitar0123!@localhost:5432/fastapi_test'

# Create engine and session
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override get_db to use the test database
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create client fixture
@pytest.fixture
def client():
    models.Base.metadata.create_all(bind=engine)  # Use models.Base instead of re-defining Base
    yield TestClient(app)
    models.Base.metadata.drop_all(bind=engine)

# Test for creating user
def test_create_user(client):
    res = client.post("/users/", json={"email": "test@gmail.com", "password": "123456"})
    new_user = schemas.UserOut(**res.json())
    print(res.json())
    assert new_user.email == "test@gmail.com"
    assert res.status_code == 200

