from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

# --- User Models ---
class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    name: Optional[str] = None
    emailVerified: bool = Field(default=False)

class User(UserBase, table=True):
    __tablename__ = "user"  # Matches BetterAuth
    id: str = Field(primary_key=True)
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(UserBase):
    password: str

class UserPublic(UserBase):
    id: str
    createdAt: datetime
    updatedAt: datetime

# --- Task Models ---
class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    priority: str = Field(default="medium")
    due_date: Optional[datetime] = Field(default=None)
    status: str = Field(default="todo")
    category: Optional[str] = Field(default="Personal")
    tags: Optional[str] = Field(default="")

class Task(TaskBase, table=True):
    __tablename__ = "Task"
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(index=True)
    completed_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TaskCreate(TaskBase):
    pass

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[datetime] = None

class TaskPublic(TaskBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

# --- Chat Models ---
class Conversation(SQLModel, table=True):
    __tablename__ = 'conversations'
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Message(SQLModel, table=True):
    __tablename__ = 'messages'
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int
    user_id: str
    role: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
