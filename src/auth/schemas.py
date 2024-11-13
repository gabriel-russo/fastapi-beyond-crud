from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import List
from src.books.schemas import Book


class UserCreateModel(BaseModel):
    username: str = Field(max_length=8)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)
    first_name: str = Field(max_length=18)
    last_name: str = Field(max_length=12)


class UserModel(BaseModel):
    uid: UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class UserBookModel(UserModel):
    books: List[Book]


class UserLoginModel(BaseModel):
    email: str
    password: str


class AccessToken(BaseModel):
    token: dict
