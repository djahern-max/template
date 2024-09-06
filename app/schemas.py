from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int
    owner: UserOut

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str   

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class User(BaseModel):
    id: int
    email: str
    is_active: bool

    class Config:
        from_attributes = True

class Vote(BaseModel):
    post_id: int
    dir: int = Field(..., le=1)

    class Config:
        from_attributes = True

class Post(BaseModel):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    id: int
    title: str
    content: str
    votes: int

    class Config:
        from_attributes = True







