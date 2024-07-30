from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app import models, schemas, database

router = APIRouter()

@router.get("/ping")
def ping():
    return {"message": "pong"}

@router.post("/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # Example user creation logic
    # Check if user already exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    # Hash the user's password (if applicable)
    # user.password = hash_password(user.password)  # Assuming hash_password is a function you've defined
    # Create the new user
    new_user = models.User(email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

