from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, utils, database

router = APIRouter(
    tags=["Users"]
)

@router.post("/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    hashed_password = utils.hash_password(user.password)
    db_user = models.User(username=user.username, password=hashed_password)  
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user



