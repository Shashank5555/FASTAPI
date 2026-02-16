from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.models import User
import sqlalchemy
from typing import Optional

# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True

# class CreatePost(BaseModel):
#     title: str
#     content: str
#     published: bool = True

# class UpdatePost(BaseModel):
#     #title: str
#     #content: str
#     published: bool

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

#This just extends the PostBase class
#without adding any extra functionality if only pass is given
class PostCreate(PostBase):
    pass



#The schema required by the user to be sent when he is creating 
# or logging into his account.
#Request model
class UserCreate(BaseModel):
    email: EmailStr
    password: str

#Response model for the response after creating a User
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

#Request model or schema for login (post) from the user
class UserLogin(BaseModel):
    email: EmailStr
    password: str



#Post class is extending the PostBase class,
#Meaning it inherits all the attributes of it
class Post(PostBase):
    # title: str
    # content: str
    # published: bool
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    # class Config:
    #     orm_mode = True



#Request model when the user provides the access token back to us
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None