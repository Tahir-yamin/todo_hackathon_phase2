# Load environment variables FIRST
# Force redeploy: Dec 23, 2025 - CORS + Trailing slash fixes
from dotenv import load_dotenv
load_dotenv()

import os

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from sqlmodel import SQLModel

# Relative imports for production deployment
from db import create_db_and_tables, engine
from routers import tasks, auth, ai, chat
from auth import get_current_user, BetterAuthUser
from models import User, Task, Conversation, Message  # Import all models for table creation

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables on startup
    create_db_and_tables()
    # NOTE: Removed SQLModel.metadata.create_all() to avoid conflicts with BetterAuth schema
    print("✅ Database connection established")
    yield


app = FastAPI(
    title="Todo API",
    description="A simple Todo API built with FastAPI",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware - WIDE OPEN FOR HACKATHON DEMO
print(f"🔧 DEBUG: Configuring CORS with WILDCARD (hackathon demo mode)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Wildcard for demo
    allow_credentials=False,  # MUST be False with wildcard
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,  # Cache preflight for 1 hour to prevent 502s
)
print(f"✅ DEBUG: CORS configured with wildcard - demo mode active")

# Request logging middleware to debug 502 errors
@app.middleware("http")
async def log_requests(request, call_next):
    print(f"📥 {request.method} {request.url.path} from {request.client.host if request.client else 'unknown'}")
    response = await call_next(request)
    print(f"📤 {request.method} {request.url.path} → {response.status_code}")
    return response

# Include the routers
app.include_router(tasks.router)
app.include_router(auth.router)
app.include_router(ai.router)  # AI-powered features
app.include_router(chat.router)  # Phase 3: AI Chatbot

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
