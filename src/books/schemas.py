from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from src.reviews.schemas import ReviewModel


class Book(BaseModel):
    uid: UUID
    title: str
    author: str
    publisher: str
    published_date: datetime
    page_count: int
    language: str
    user_uid: UUID
    created_at: datetime
    updated_at: datetime


class BookDetailModel(Book):
    reviews: List[ReviewModel]


class BookCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str


class BookUpdateModel(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    page_count: Optional[str] = None
    language: Optional[str] = None
