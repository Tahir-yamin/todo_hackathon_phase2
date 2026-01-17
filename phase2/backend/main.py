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
    
    # NOW SAFE: Create all tables with clean model definitions
    SQLModel.metadata.create_all(engine)
    print("✅ All database tables created/verified")
    print("✅ Database connection established")
    
    # Phase 5: Minimal event bus (zero dependencies)
    try:
        from simple_events import event_bus
        print("✅ Lightweight event bus loaded")
    except Exception as e:
        print(f"⚠️ Event bus not loaded: {e}")
    
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

# ========== AGENTIC INTERFACE (MCP Protocol) ==========
# Evolution Tool Hub endpoints for Antigravity Agent

from tools import tool_hub
from typing import Dict, Any
from fastapi import Body

@app.get("/agent/tools")
async def list_agent_skills():
    """
    MCP Discovery Endpoint: Returns the complete tool manifest.
    The Antigravity agent calls this to discover available capabilities.
    """
    return {
        "protocol": "MCP",
        "version": "1.0.0",
        "tools": tool_hub.get_tool_manifest()
    }

@app.post("/agent/execute")
async def run_agent_skill(payload: Dict[str, Any] = Body(...)):
    """
    MCP Execution Endpoint: Executes a tool by name with provided arguments.
    
    Expected payload:
    {
        "name": "tool_name",
        "arguments": { ... }
    }
    """
    tool_name = payload.get("name")
    arguments = payload.get("arguments", {})
    
    if not tool_name:
        return {
            "status": "error",
            "message": "Missing 'name' in payload"
        }
    
    result = await tool_hub.execute(tool_name, arguments)
    return result

@app.get("/agent/health")
async def agent_health_check():
    """Quick health check specifically for the agentic interface"""
    return {
        "status": "operational",
        "tools_available": len(tool_hub.get_tool_manifest()),
        "protocol": "MCP"
    }

# ========== DOCKER SKILLS (MCP Protocol) ==========
# Docker-Architect capabilities for build optimization and debugging

from docker_skills import docker_skills

@app.get("/docker/skills")
async def list_docker_skills():
    """
    MCP Discovery Endpoint for Docker capabilities.
    Returns available Docker management skills.
    """
    return {
        "protocol": "MCP",
        "agent": "Docker-Architect",
        "skills": [
            "analyze_container_stats",
            "verify_prisma_binary",
            "analyze_image_layers",
            "detect_build_failures",
            "suggest_dockerfile_fixes",
            "compare_image_sizes",
            "check_security_vulnerabilities",
            "optimize_build_cache"
        ]
    }

@app.post("/docker/analyze-stats")
async def analyze_container_stats(payload: Dict[str, Any] = Body(...)):
    """Get real-time resource statistics for a container"""
    container_name = payload.get("container_name")
    if not container_name:
        return {"status": "error", "message": "Missing container_name"}
    
    return docker_skills.analyze_container_stats(container_name)

@app.post("/docker/verify-prisma")
async def verify_prisma(payload: Dict[str, Any] = Body(...)):
    """Verify Prisma binary exists in container"""
    container_name = payload.get("container_name")
    if not container_name:
        return {"status": "error", "message": "Missing container_name"}
    
    return docker_skills.verify_prisma_binary(container_name)

@app.post("/docker/analyze-layers")
async def analyze_layers(payload: Dict[str, Any] = Body(...)):
    """Analyze image layers for optimization opportunities"""
    image_name = payload.get("image_name")
    if not image_name:
        return {"status": "error", "message": "Missing image_name"}
    
    return docker_skills.analyze_image_layers(image_name)

@app.post("/docker/detect-failures")
async def detect_failures(payload: Dict[str, Any] = Body(...)):
    """Detect common build failure patterns"""
    build_log = payload.get("build_log")
    if not build_log:
        return {"status": "error", "message": "Missing build_log"}
    
    return docker_skills.detect_build_failures(build_log)

@app.post("/docker/suggest-fixes")
async def suggest_fixes(payload: Dict[str, Any] = Body(...)):
    """Suggest Dockerfile improvements"""
    dockerfile_path = payload.get("dockerfile_path")
    detected_issues = payload.get("detected_issues", [])
    
    if not dockerfile_path:
        return {"status": "error", "message": "Missing dockerfile_path"}
    
    return docker_skills.suggest_dockerfile_fixes(dockerfile_path, detected_issues)

@app.post("/docker/compare-sizes")
async def compare_sizes(payload: Dict[str, Any] = Body(...)):
    """Compare image sizes before and after optimization"""
    image_before = payload.get("image_before")
    image_after = payload.get("image_after")
    
    if not image_before or not image_after:
        return {"status": "error", "message": "Missing image_before or image_after"}
    
    return docker_skills.compare_image_sizes(image_before, image_after)

@app.post("/docker/security-scan")
async def security_scan(payload: Dict[str, Any] = Body(...)):
    """Basic security check for Docker image"""
    image_name = payload.get("image_name")
    if not image_name:
        return {"status": "error", "message": "Missing image_name"}
    
    return docker_skills.check_security_vulnerabilities(image_name)

@app.post("/docker/optimize-cache")
async def optimize_cache(payload: Dict[str, Any] = Body(...)):
    """Analyze Dockerfile for cache optimization"""
    dockerfile_path = payload.get("dockerfile_path")
    if not dockerfile_path:
        return {"status": "error", "message": "Missing dockerfile_path"}
    
    return docker_skills.optimize_build_cache(dockerfile_path)

if __name__ == "__main__":
    import uvicorn
    # Respect Railway's dynamic PORT assignment
    port = int(os.getenv("PORT", 8080))  # Default to 8080 to match uvicorn default
    uvicorn.run(app, host="0.0.0.0", port=port)
