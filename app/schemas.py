from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


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




# creating users
class Create_user(BaseModel):
    email : EmailStr
    password: str

class User_response(BaseModel):
    id : int
    email: EmailStr
    class Config:
        orm_mode = True

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
