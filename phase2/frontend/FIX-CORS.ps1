# CORS FIX - Simple Version (No Syntax Errors)

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "CORS FIX - Clearing All Caches" -ForegroundColor Cyan  
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Navigate to frontend
Set-Location "d:\Hackathon phase 1 TODO App\todo_hackathon_phase1\phase2\frontend"

# Delete Next.js build cache
Write-Host "Deleting .next cache folder..." -ForegroundColor Yellow
if (Test-Path .next) {
    Remove-Item -Recurse -Force .next
    Write-Host "Done: Deleted .next folder" -ForegroundColor Green
} else {
    Write-Host "Warning: .next folder not found" -ForegroundColor Yellow
}

# Delete node_modules cache
Write-Host ""
Write-Host "Deleting node_modules cache..." -ForegroundColor Yellow
if (Test-Path node_modules/.cache) {
    Remove-Item -Recurse -Force node_modules/.cache
    Write-Host "Done: Deleted node_modules/.cache" -ForegroundColor Green
}

# Show current environment variables
Write-Host ""
Write-Host "Current environment variables:" -ForegroundColor Cyan
Get-Content .env.local | Select-String "NEXT_PUBLIC"

# Start dev server
Write-Host ""
Write-Host "Starting dev server..." -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

npm run dev
