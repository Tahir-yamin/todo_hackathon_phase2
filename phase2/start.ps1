# Unified PowerShell script to start both backend and frontend
# Similar to start.sh but for Windows PowerShell

Write-Host "Starting Todo Application..." -ForegroundColor Green

# Set Python path to include parent directory
$env:PYTHONPATH = $PSScriptRoot

# Load environment variables from .env file
Write-Host "Loading environment variables..." -ForegroundColor Yellow
Get-Content "$PSScriptRoot\backend\.env" | ForEach-Object {
    if ($_ -match '^([^#].+?)=(.*)$') {
        [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2], 'Process')
    }
}

# Start Backend
Write-Host "Starting backend server on port 8002..." -ForegroundColor Yellow
$backendJob = Start-Job -ScriptBlock {
    param($scriptRoot)
    Set-Location $scriptRoot
    $env:PYTHONPATH = $scriptRoot
    
    # Load environment variables in the job
    Get-Content "backend\.env" | ForEach-Object {
        if ($_ -match '^([^#].+?)=(.*)$') {
            [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2], 'Process')
        }
    }
    
    & "backend\venv\Scripts\python.exe" -m backend.main
} -ArgumentList $PSScriptRoot

Start-Sleep -Seconds 5

# Start Frontend
Write-Host "Starting frontend server on port 3002..." -ForegroundColor Yellow
$frontendJob = Start-Job -ScriptBlock {
    param($scriptRoot)
    Set-Location "$scriptRoot\frontend"
    npm run dev -- -p 3002
} -ArgumentList $PSScriptRoot

Start-Sleep -Seconds 3

Write-Host "`nBoth services are running!" -ForegroundColor Green
Write-Host "Backend:  http://localhost:8002" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:3002" -ForegroundColor Cyan
Write-Host "`nPress Ctrl+C to stop both services.`n" -ForegroundColor Yellow

# Monitor jobs and display output
try {
    while ($true) {
        Receive-Job -Job $backendJob
        Receive-Job -Job $frontendJob
        
        if ($backendJob.State -eq 'Failed' -or $frontendJob.State -eq 'Failed') {
            Write-Host "One of the services failed!" -ForegroundColor Red
            break
        }
        
        Start-Sleep -Milliseconds 500
    }
}
finally {
    Write-Host "`nStopping services..." -ForegroundColor Yellow
    Stop-Job -Job $backendJob, $frontendJob
    Remove-Job -Job $backendJob, $frontendJob -Force
    Write-Host "All services stopped." -ForegroundColor Green
}
