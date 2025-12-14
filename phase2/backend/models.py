from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid


# User models (for auth router compatibility)
class UserBase(SQLModel):
    username: str = Field(min_length=3, max_length=50)
    email: str = Field(regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class User(UserBase, table=True):
    __tablename__ = "users"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)


class UserPublic(SQLModel):
    id: uuid.UUID
    username: str
    email: str
    created_at: datetime
    updated_at: datetime
    is_active: bool


# Task models
class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    priority: str = Field(default="medium", regex=r'^(low|medium|high)$')
    due_date: Optional[datetime] = Field(default=None)
    status: str = Field(default="pending", regex=r'^(pending|completed)$')
    category: Optional[str] = Field(default="Personal", max_length=50)
    tags: Optional[str] = Field(default="", max_length=500)


class TaskCreate(TaskBase):
    pass


class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    priority: Optional[str] = Field(default=None, regex=r'^(low|medium|high)$')
    due_date: Optional[datetime] = Field(default=None)
    status: Optional[str] = Field(default=None, regex=r'^(pending|completed)$')
    category: Optional[str] = Field(default=None, max_length=50)
    tags: Optional[str] = Field(default=None, max_length=500)


class Task(TaskBase, table=True):
    __tablename__ = "Task"  # Match database table name

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str  # Match Better Auth user table (TEXT not UUID)
    completed_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskPublic(TaskBase):
    id: str
    user_id: str
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime