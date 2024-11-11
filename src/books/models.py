from sqlmodel import SQLModel, Field, Column
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from datetime import datetime
from uuid import UUID as py_UUID, uuid4


class Book(SQLModel, table=True):
    __tablename__ = "books"

    uid: py_UUID = Field(sa_column=Column(UUID, primary_key=True, default=uuid4))
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str
    created_at: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now))

    def __repr__(self):
        return f"<Book {self.title}>"
