from sqlmodel import SQLModel, Field, Column, Relationship
from typing import Optional
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from datetime import datetime
from uuid import UUID as py_UUID, uuid4
from src.auth import models


class Book(SQLModel, table=True):
    __tablename__ = "books"

    uid: py_UUID = Field(
        sa_column=Column(UUID, nullable=False, primary_key=True, default=uuid4)
    )
    title: str
    author: str
    publisher: str
    published_date: datetime
    page_count: int
    language: str
    user_uid: Optional[py_UUID] = Field(default=None, foreign_key="users.uid")
    created_at: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now))
    user: Optional["models.User"] = Relationship(back_populates="books")

    def __repr__(self):
        return f"<Book {self.title}>"
