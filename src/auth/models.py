from sqlmodel import SQLModel, Field, Column
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP, VARCHAR
from uuid import UUID as py_UUID, uuid4
from datetime import datetime


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

    def __repr__(self) -> str:
        return f"<User {self.username}>"
