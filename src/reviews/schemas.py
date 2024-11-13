from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID


class ReviewModel(BaseModel):
    uid: UUID
    rating: int = Field(le=5)
    review_text: str
    user_uid: Optional[UUID]
    book_uid: Optional[UUID]
    created_at: datetime
    updated_at: datetime


class ReviewCreateModel(BaseModel):
    rating: int = Field(le=5)
    review_text: str
