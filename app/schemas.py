from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
import random


# post model, this is what a post should have
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

# creating a post
class PostCreate(PostBase):
    pass

# response from the api to the user
class User_response(BaseModel):
    id : int
    email: EmailStr
    created_at : datetime
    class Config:
        orm_mode = True

# api response
class Post_response(PostBase):
    """
    this structures the post the api sends back
    """
    id : int
    owner_id : int
    created_at: datetime
    owner: User_response
    class Config:
        orm_mode = True




# creating users
class Create_user(BaseModel):
    email : EmailStr
    password: str



# user login model
class User_login(BaseModel):
    email: EmailStr
    password : str

# token model
class Token(BaseModel):
    access_token:str
    token_type: str

# token data
class TokenData(BaseModel):
    id: Optional[str] = None
    exp: Optional[datetime]

# like system
class Vote(BaseModel):
    post_id : int
    vote_direction : int = random.choice((1,0))


# class Post_likes(PostBase): #returning a post with likes
#     Post : Post_response
#     likes : int
#
#     class Config:
#         orm_mode = True
