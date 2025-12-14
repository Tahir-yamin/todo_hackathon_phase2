# Phase II: Full-Stack Todo Application

A production-ready web application with Python FastAPI backend and React (Next.js) frontend.

## Description

This is the Phase II implementation - a complete full-stack web application with authentication, database persistence, and a modern UI.

## Features

- ✅ User authentication (sign up, login, logout)
- ✅ Create, read, update, delete tasks
- ✅ Mark tasks as complete/incomplete
- ✅ Task filtering and search
- ✅ Priority levels
- ✅ Due dates
- ✅ Tags/categories
- ✅ Database persistence (PostgreSQL)
- ✅ RESTful API
- ✅ Modern React UI

## Prerequisites

- Python 3.13+
- Node.js 18+
- PostgreSQL database (or Neon serverless)

## Quick Start

### For Complete Instructions
See [START_GUIDE.md](START_GUIDE.md) for detailed startup instructions for all platforms (Windows, Linux, WSL).

### Quick Start (Linux/Mac/WSL)
```bash
cd phase2
./start.sh
```

### Quick Start (Windows PowerShell)
```powershell
cd phase2
.\start.ps1
```

The application will be available at:
- **Frontend**: http://localhost:3002
- **Backend API**: http://localhost:8002
- **API Docs**: http://localhost:8002/docs

## Project Structure

```
phase2/
├── backend/              # FastAPI backend
│   ├── main.py          # Application entry point
│   ├── db.py            # Database configuration
│   ├── models.py        # Data models
│   ├── auth.py          # Authentication
│   └── routers/         # API endpoints
├── frontend/            # Next.js React frontend
│   ├── src/            # Source code
│   └── package.json    # Dependencies
├── scripts/            # Database setup scripts
├── docs/               # Documentation
├── start.sh            # Startup script (Linux/Mac/WSL)
├── start.ps1           # Unified startup (PowerShell)
└── START_GUIDE.md      # Complete startup guide
```

## Setup

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Setup
```bash
cd frontend
npm install
```

### Environment Configuration

1. **Backend**: Copy `backend/.env.example` to `backend/.env` and configure:
   - `DATABASE_URL` - PostgreSQL connection string
   - `BETTER_AUTH_SECRET` - Authentication secret

2. **Frontend**: Copy `frontend/.env.local.example` to `frontend/.env.local` and configure:
   - `NEXT_PUBLIC_APP_URL` - Frontend URL (http://localhost:3002)
   - `NEXT_PUBLIC_API_URL` - Backend URL (http://localhost:8002)
   - `BETTER_AUTH_SECRET` - Must match backend secret

## API Documentation

Once running, access:
- Swagger UI: http://localhost:8002/docs
- ReDoc: http://localhost:8002/redoc

## Technology Stack

**Backend:**
- FastAPI (Python web framework)
- SQLModel (ORM)
- PostgreSQL (Database)
- Better Auth (Authentication)
- Uvicorn (ASGI server)

**Frontend:**
- Next.js 14 (React framework)
- TypeScript
- Tailwind CSS
- Axios (HTTP client)
- Better Auth client

## Additional Documentation

- [START_GUIDE.md](START_GUIDE.md) - Complete startup guide for all platforms
- [docs/SETUP_GUIDE.md](docs/SETUP_GUIDE.md) - Detailed setup instructions
- [docs/MANUAL_DB_SETUP.md](docs/MANUAL_DB_SETUP.md) - Database setup
- [docs/BETTER_AUTH_IMPLEMENTATION.md](docs/BETTER_AUTH_IMPLEMENTATION.md) - Auth implementation details
