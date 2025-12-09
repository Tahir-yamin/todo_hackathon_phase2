# Todo Application

A full-stack todo application with a Python FastAPI backend and a React frontend.

## Prerequisites

- Python 3.13+
- Node.js 18+ (with npm)

## Setup

### Backend Setup

1. Create and activate a Python virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install backend dependencies:

```bash
pip install -r backend/requirements.txt
```

### Frontend Setup

1. Navigate to the frontend directory:

```bash
cd frontend
```

2. Install frontend dependencies:

```bash
npm install
```

## Running the Application

### Method 1: Using the start script (Recommended)

Run the application using the provided start script that launches both the backend and frontend concurrently:

```bash
chmod +x start.sh
./start.sh
```

The backend will be available at `http://localhost:8000` and the frontend at `http://localhost:3000`.

### Method 2: Manual start

1. **Start the backend:**

```bash
cd backend
python main.py
```

The backend API will be available at `http://localhost:8000`.

2. **Start the frontend:**

In a new terminal window:

```bash
cd frontend
npm run dev
```

The frontend will be available at `http://localhost:3000`.

## API Documentation

Once the backend is running, you can access the API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
.
├── backend/              # FastAPI backend
│   ├── main.py          # Main application entry point
│   ├── db.py            # Database configuration
│   ├── models.py        # Database models
│   └── routers/         # API route handlers
├── frontend/             # React frontend
│   ├── src/             # Source code
│   ├── package.json     # Frontend dependencies
│   └── next.config.js   # Next.js configuration
├── start.sh              # Script to start both backend and frontend
└── README.md            # This file
```