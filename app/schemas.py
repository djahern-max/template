from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from pydantic import ConfigDict


class UserOut(BaseModel):
    id: int
    username: str  
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


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

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str 
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class User(BaseModel):
    id: int
    username: str 
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class Vote(BaseModel):
    post_id: int
    dir: int = Field(..., le=1)

    model_config = ConfigDict(from_attributes=True)


class Post(BaseModel):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    model_config = ConfigDict(from_attributes=True)


class PostOut(BaseModel):
    id: int
    title: str
    content: str
    votes: int

    model_config = ConfigDict(from_attributes=True)









