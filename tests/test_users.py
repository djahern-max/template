from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine, engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app import schemas, models
from app.database import get_db




SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Guitar0123!@localhost:5432/fastapi_test'
# SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"


engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)


# def test_root():
#     res = client.get("/")
#     print(res.json().get('message'))
#     assert res.json().get('message') == "Welcome to ryze!"
#     assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/", json={"email": "test@gmail.com", "password": "123456"})
    new_user = schemas.UserOut(**res.json())
    print(res.json())
    assert new_user.email == "test@gmail.com"
    assert res.status_code == 200

