from pydantic import BaseModel
from datetime import datetime


# post model
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

# creating a post
class PostCreate(PostBase):
    pass


# api response
class Post_response(PostBase):
    """
    this structures the data the api sends back
    """
    id: int
    # created_at: datetime
    class Config:
        orm_mode = True
