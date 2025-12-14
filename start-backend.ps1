# Set Python path to include parent directory
$env:PYTHONPATH = "d:\Hackathon phase 1 TODO App\todo_hackathon_phase1"

# Load environment variables from .env file
Get-Content "d:\Hackathon phase 1 TODO App\todo_hackathon_phase1\backend\.env" | ForEach-Object {
    if ($_ -match '^([^#].+?)=(.*)$') {
        [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2], 'Process')
    }
}

# Change to project root directory
cd "d:\Hackathon phase 1 TODO App\todo_hackathon_phase1"

# Activate virtual environment and run the backend server
& "backend\venv\Scripts\python.exe" -m backend.main
