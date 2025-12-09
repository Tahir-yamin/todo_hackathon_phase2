#!/bin/bash

# Exit on any error
set -e

cleanup() {
    echo
    echo "Shutting down services..."
    if [ ! -z "$BACKEND_PID" ]; then kill $BACKEND_PID 2>/dev/null || true; fi
    if [ ! -z "$FRONTEND_PID" ]; then kill $FRONTEND_PID 2>/dev/null || true; fi
    echo "All services stopped."
    exit 0
}

trap cleanup SIGINT SIGTERM EXIT

echo "Starting Todo Application..."

# --- START BACKEND ---
echo "Starting backend server..."
source backend/venv/bin/activate

# Load environment variables from .env file
while IFS= read -r line; do
    if [[ $line =~ ^[^#].*= ]]; then
        export "$line"
    fi
done < backend/.env

# CRITICAL FIX: Add current directory to Python path so 'import backend' works
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Run uvicorn from the root directory with the correct module path and port
uvicorn backend.main:app --host 0.0.0.0 --port 8001 --reload &
BACKEND_PID=$!
sleep 5 # Wait for backend to initialize

# --- START FRONTEND ---
echo "Starting frontend server..."
cd frontend
# Install dependencies if they are missing (optional check)
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi
npx next dev -p 3001 &
FRONTEND_PID=$!
cd ..

echo "Both services are running!"
echo "Backend: http://localhost:8001"
echo "Frontend: http://localhost:3001"
echo "Press Ctrl+C to stop."

wait $BACKEND_PID $FRONTEND_PID
