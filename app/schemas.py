from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


# Define schema for posts
# The Pydantic model defines the structure of request and response,
# used to verify that the expected fields and field types are present
class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # default value
    # rating: Optional[int] = None  # mark field as optional


class PostBase(BaseModel):
    title: str
    content: str


# Create and Update can have different models,
# based on the user's ability to create posts with default values or not
class PostCreate(PostBase):
    published: bool = True  # default value


class PostUpdate(PostBase):
    published: bool


# Defined before PostResponse
class UserResponse(BaseModel):
    id: int
    email: EmailStr  # validates email format
    created_at: datetime

    class Config:
        orm_mode = True


class PostResponse(PostBase):
    id: int
    published: bool
    created_at: datetime
    owner_id: int

    # Since owner was added to the Post model, we need to add that property in the schema as well.
    # In order to be verified ny static analysis, the class type needs to be defined before
    owner: UserResponse

    # This inner class is required in the response model, because the db_query returns an object that
    # is not really a dictionary, and pydantic only works with dictionaries.
    # This class allows pydantic to work with other objects besides dictionaries, for this class.
    class Config:
        orm_mode = True


# In order to retrieve the number of votes for each post,
# we need to define a new response model
class PostWithVotesResponse(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr  # validates email format
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) # anything less than 1 is allowed (negative numbers are also allowed)
