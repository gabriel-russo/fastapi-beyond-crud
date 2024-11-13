from sqlmodel import SQLModel, Field, Column, Relationship
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP, VARCHAR
from uuid import UUID as py_UUID, uuid4
from datetime import datetime
from typing import List, Optional


class User(SQLModel, table=True):
    __tablename__ = "users"

    uid: py_UUID = Field(
        sa_column=Column(UUID, nullable=False, primary_key=True, default=uuid4)
    )
    username: str
    email: str
    password_hash: str = Field(exclude=True)
    first_name: str
    last_name: str
    role: str = Field(sa_column=Column(VARCHAR, nullable=False, server_default="user"))
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now))
    books: List["Book"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )
    reviews: List["Review"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self) -> str:
        return f"<User {self.username}>"


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
    user: Optional["User"] = Relationship(back_populates="books")
    reviews: List["Review"] = Relationship(
        back_populates="books", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self):
        return f"<Book {self.title}>"


class Review(SQLModel, table=True):
    __tablename__ = "reviews"

    uid: py_UUID = Field(
        sa_column=Column(UUID, nullable=False, primary_key=True, default=uuid4)
    )
    rating: int = Field(lt=5)
    review_text: str
    user_uid: Optional[py_UUID] = Field(default=None, foreign_key="users.uid")
    book_uid: Optional[py_UUID] = Field(default=None, foreign_key="books.uid")
    created_at: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now))
    user: Optional["User"] = Relationship(back_populates="reviews")
    book: Optional["Book"] = Relationship(back_populates="reviews")

    def __repr__(self):
        return f"<Review for book {self.book_uid} by user {self.user_uid}>"
