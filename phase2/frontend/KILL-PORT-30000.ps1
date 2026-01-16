# ZOMBIE PROCESS KILLER - Port 30000

# Step 1: Find the process using port 30000
Write-Host "`nSearching for process on port 30000..." -ForegroundColor Yellow
$processInfo = netstat -ano | findstr :30000

if ($processInfo) {
    Write-Host "Found process on port 30000:" -ForegroundColor Red
    Write-Host $processInfo
    
    # Extract PID (last column)
    $pid = ($processInfo -split '\s+')[-1]
    Write-Host "`nProcess ID (PID): $pid" -ForegroundColor Cyan
    
    # Get process details
    $process = Get-Process -Id $pid -ErrorAction SilentlyContinue
    if ($process) {
        Write-Host "Process Name: $($process.ProcessName)" -ForegroundColor Cyan
        Write-Host "Start Time: $($process.StartTime)" -ForegroundColor Cyan
        
        # Kill it
        Write-Host "`nKilling process..." -ForegroundColor Yellow
        Stop-Process -Id $pid -Force
        Write-Host "Process killed!" -ForegroundColor Green
    }
} else {
    Write-Host "No process found on port 30000" -ForegroundColor Green
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Now restart your frontend on port 3002"
Write-Host "cd 'd:\Hackathon phase 1 TODO App\todo_hackathon_phase1\phase2\frontend'"
Write-Host "npm run dev"
Write-Host "========================================`n" -ForegroundColor Cyan
