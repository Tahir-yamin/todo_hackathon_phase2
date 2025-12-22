from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import HTTPException, Depends, Request, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from sqlmodel import Session, select, SQLModel, Field
from db import get_session
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
    request: Request,
    session: Session = Depends(get_session)
) -> BetterAuthUser:
    """Get current user from X-User-ID header (set by Better Auth frontend)."""
    
    # 1. Try Header (Priority for hackathon - port mismatch workaround)
    user_id = request.headers.get("X-User-ID", request.headers.get("x-user-id"))
    if user_id:
        # Dynamically create user object from header (no DB lookup needed)
        return BetterAuthUser(
            id=user_id,
            email=f"{user_id}@app.com",
            name=user_id.split('@')[0] if '@' in user_id else user_id[:10],
            emailVerified=True,
            image=None,
            createdAt=datetime.now(),
            updatedAt=datetime.now()
        )
    
    # 2. Try Cookie (Fallback for traditional better-auth)
    token = request.cookies.get("better-auth.session_token")
    if token:
        # Could validate token here, but for hackathon we trust it
        return BetterAuthUser(
            id="cookie_user",
            email="cookie@test.com",
            name="Cookie User",
            emailVerified=True,
            image=None,
            createdAt=datetime.now(),
            updatedAt=datetime.now()
        )
    
    # 3. Dev fallback (for Swagger testing)
    print("⚠️  DEV MODE: No header or cookie, using dev_user_123")
    return BetterAuthUser(
        id="dev_user_123",
        email="dev@test.com",
        name="Dev User",
        emailVerified=True,
        image=None,
        createdAt=datetime.now(),
        updatedAt=datetime.now()
    )