from sqlmodel import SQLModel, Field
from typing import Optional, List
from datetime import datetime
from pydantic import field_validator
import uuid
import json

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

# --- Task Models (Phase 5 Enhanced) ---
class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    priority: str = Field(default="medium")  # high, medium, low
    due_date: Optional[datetime] = Field(default=None)
    status: str = Field(default="todo")
    category: Optional[str] = Field(default="Personal")
    tags: Optional[str] = Field(default="")  # Comma-separated tags
    
    # Phase 5: Recurrence fields (matching Prisma schema)
    recurrence: str = Field(default="NONE")  # NONE, DAILY, WEEKLY, MONTHLY, YEARLY
    next_occurrence: Optional[datetime] = Field(default=None)  # Next scheduled occurrence

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
    category: Optional[str] = None
    tags: Optional[str] = None
    
    # Phase 5: Recurrence updates (matching Prisma)
    recurrence: Optional[str] = None
    next_occurrence: Optional[datetime] = None

class TaskPublic(TaskBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    next_occurrence: Optional[datetime] = None
    completed_at: Optional[datetime] = None

# --- Task Filter Model (Phase 5) ---
class TaskFilter(SQLModel):
    """Filter parameters for listing tasks."""
    status: Optional[str] = None
    priority: Optional[str] = None
    due_before: Optional[datetime] = None
    due_after: Optional[datetime] = None
    tags: Optional[str] = None  # Comma-separated tags to filter
    has_recurrence: Optional[bool] = None
    sort_by: str = "created_at"  # created_at, due_date, priority, title
    sort_order: str = "desc"  # asc, desc

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

