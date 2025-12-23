from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid


# ============================================================================
# USER MODELS - Single Source of Truth for BetterAuth Integration
# ============================================================================

class User(SQLModel, table=True):
    """
    User model compatible with BetterAuth.
    Uses 'users' (plural) to avoid PostgreSQL 'user' reserved keyword.
    """
    __tablename__ = "users"
    
    id: str = Field(primary_key=True)
    email: str = Field(unique=True, index=True)
    name: str
    emailVerified: bool = False
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    tasks: List["Task"] = Relationship(back_populates="user")


class UserPublic(SQLModel):
    """Public user representation (no sensitive data)"""
    id: str
    name: str
    email: str
    createdAt: datetime


# ============================================================================
# TASK MODELS
# ============================================================================

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    priority: str = Field(default="medium", regex=r'^(low|medium|high)$')
    due_date: Optional[datetime] = Field(default=None)
    status: str = Field(default="todo", regex=r'^(todo|in_progress|completed)$')
    category: Optional[str] = Field(default="Personal", max_length=50)
    tags: Optional[str] = Field(default="", max_length=500)


class TaskCreate(TaskBase):
    pass


class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    priority: Optional[str] = Field(default=None, regex=r'^(low|medium|high)$')
    due_date: Optional[datetime] = Field(default=None)
    status: Optional[str] = Field(default=None, regex=r'^(todo|in_progress|completed)$')
    category: Optional[str] = Field(default=None, max_length=50)
    tags: Optional[str] = Field(default=None, max_length=500)


class Task(TaskBase, table=True):
    __tablename__ = "tasks"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    completed_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    user: Optional[User] = Relationship(back_populates="tasks")


class TaskPublic(TaskBase):
    id: str
    user_id: str
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime


# ============================================================================
# CONVERSATION MODELS (Phase 3: AI Chatbot)
# ============================================================================

class Conversation(SQLModel, table=True):
    __tablename__ = 'conversations'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Message(SQLModel, table=True):
    __tablename__ = 'messages'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key='conversations.id', index=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    role: str = Field()  # 'user' or 'model'
    content: str = Field()
    created_at: datetime = Field(default_factory=datetime.utcnow)
