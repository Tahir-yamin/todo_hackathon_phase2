from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import HTTPException, Depends, Request, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from sqlmodel import Session, select, SQLModel, Field
from backend.db import get_session
import os

# Simple User model matching Better Auth's user table
class BetterAuthUser(SQLModel, table=True):
    __tablename__ = "user"
    
    id: str = Field(primary_key=True)
    email: str
    name: Optional[str] = None
    emailVerified: bool = False
    image: Optional[str] = None
    createdAt: datetime
    updatedAt: datetime

# Security settings
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(
    x_user_id: Optional[str] = Header(None),
    session: Session = Depends(get_session)
) -> BetterAuthUser:
    """Get current user from X-User-ID header (set by Better Auth frontend)."""
    
    if not x_user_id:
        raise HTTPException(
            status_code=401,
            detail="X-User-ID header required",
        )
    
    # Get user from Better Auth user table
    statement = select(BetterAuthUser).where(BetterAuthUser.id == x_user_id)
    user = session.exec(statement).first()
    
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found in database",
        )
    
    return user