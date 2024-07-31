from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, database, oauth2

router = APIRouter(
    tags=["Posts"],
)

@router.get("/", response_model=list[schemas.PostResponse])
def read_posts(db: Session = Depends(database.get_db)):
    posts = db.query(models.Post).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    # This line ensures that a user must be logged in to create a post
    new_post = models.Post(**post.dict(), user_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.PostResponse)
def read_post(id: int, db: Session = Depends(database.get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_post(id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Optional: Check if the current user is the owner of the post
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to delete this post")
    
    db.delete(post)
    db.commit()
    return {"message": "Post successfully deleted"}

@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(
    id: int, 
    updated_post: schemas.PostCreate, 
    db: Session = Depends(database.get_db), 
    current_user: schemas.User = Depends(oauth2.get_current_user)
):
    # Retrieve the post to be updated
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    # Check if the post exists
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Ensure the current user is the owner of the post
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to update this post")
    
    # Update the post
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post

