# Load environment variables FIRST
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

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables on startup
    create_db_and_tables()
    # Force-create all SQLModel tables (including User)
    SQLModel.metadata.create_all(engine)
    print("✅ All database tables created/verified")
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
)
print(f"✅ DEBUG: CORS configured with wildcard - demo mode active")

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
