from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, Union
from datetime import datetime
import uuid


class UserBase(SQLModel):
    username: str = Field(min_length=3, max_length=50, unique=True)
    email: str = Field(regex=r'^[\w\.-]+@[\w\.-]+\.\w+$', unique=True)


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserUpdate(SQLModel):
    username: Optional[str] = Field(default=None, min_length=3, max_length=50)
    email: Optional[str] = Field(default=None, regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')


class User(UserBase, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)

    # Relationship
    tasks: List["Task"] = Relationship(back_populates="user")


class UserPublic(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    is_active: bool


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    priority: str = Field(default="medium", regex=r'^(low|medium|high)$')
    due_date: Optional[datetime] = Field(default=None)
    status: str = Field(default="pending", regex=r'^(pending|completed)$')


class TaskCreate(TaskBase):
    pass


class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    priority: Optional[str] = Field(default=None, regex=r'^(low|medium|high)$')
    due_date: Optional[Union[datetime, str]] = Field(default=None)
    status: Optional[str] = Field(default=None, regex=r'^(pending|completed)$')


class Task(TaskBase, table=True):
    __tablename__ = "tasks"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id")
    completed_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    user: "User" = Relationship(back_populates="tasks")


class TaskPublic(TaskBase):
    id: uuid.UUID
    user_id: uuid.UUID
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime