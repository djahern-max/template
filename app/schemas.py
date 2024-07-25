from pydantic import BaseModel
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime  # Use datetime here for automatic conversion

    class Config:
        orm_mode = True  # This tells Pydantic to treat SQLAlchemy models as dict-like objects

