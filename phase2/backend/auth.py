from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import HTTPException, Depends, Request, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from sqlmodel import Session, select
from db import get_session
import os

# Import User model from models.py (aliased as BetterAuthUser for compatibility)
from models import User as BetterAuthUser

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

def decode_token(token: str):
    """Decode and verify a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

# HTTP Bearer security scheme
security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> BetterAuthUser:
    """Get the current authenticated user from JWT token."""
    token = credentials.credentials
    payload = decode_token(token)
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
   
    user = session.get(BetterAuthUser, user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# For BetterAuth compatibility - get user from X-User-ID header
async def get_user_from_header(
    x_user_id: Optional[str] = Header(None),
    session: Session = Depends(get_session)
) -> Optional[BetterAuthUser]:
    """Get user from X-User-ID header (BetterAuth compatibility)."""
    if not x_user_id:
        return None
    
    user = session.get(BetterAuthUser, x_user_id)
    return user

async def get_current_user_optional(
    request: Request,
    session: Session = Depends(get_session)
) -> Optional[BetterAuthUser]:
    """Get current user if authenticated, None otherwise."""
    try:
        # Try to get from header first
        user_id = request.headers.get("X-User-ID")
        if user_id:
            return session.get(BetterAuthUser, user_id)
        
        # Try to get from Authorization header
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            payload = decode_token(token)
            user_id = payload.get("sub")
            if user_id:
                return session.get(BetterAuthUser, user_id)
    except:
        pass
    return None