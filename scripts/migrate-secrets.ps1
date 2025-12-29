# Migration Script: Move secrets from docker-compose.yml to .env
# Run this to create .env file with current secrets

Write-Host "`n🔧 Migrating Secrets to .env File...`n" -ForegroundColor Cyan

$envPath = "phase4\docker\.env"
$examplePath = "phase4\docker\.env.example"

# Check if .env already exists
if (Test-Path $envPath) {
    Write-Host "⚠️  .env file already exists at $envPath" -ForegroundColor Yellow
    Write-Host "Do you want to overwrite it? (y/n): " -NoNewline
    $overwrite = Read-Host
    
    if ($overwrite -ne 'y' -and $overwrite -ne 'Y') {
        Write-Host "`n❌ Migration cancelled.`n" -ForegroundColor Red
        exit 0
    }
}

# Copy from example
if (Test-Path $examplePath) {
    Copy-Item $examplePath -Destination $envPath
    Write-Host "✅ Created .env from .env.example" -ForegroundColor Green
}
else {
    Write-Host "❌ .env.example not found!" -ForegroundColor Red
    exit 1
}

# Now update with actual values from your docker-compose.yml
Write-Host "`n📝 Please update the following values in phase4\docker\.env:" -ForegroundColor Yellow
Write-Host "  1. DATABASE_URL (current values are in docker-compose.yml)" -ForegroundColor Yellow
Write-Host "  2. OPENROUTER_API_KEY" -ForegroundColor Yellow
Write-Host "  3. BETTER_AUTH_SECRET" -ForegroundColor Yellow
Write-Host "  4. GITHUB_CLIENT_ID" -ForegroundColor Yellow
Write-Host "  5. GITHUB_CLIENT_SECRET" -ForegroundColor Yellow

Write-Host "`n💡 After updating .env, run:" -ForegroundColor Cyan
Write-Host "  cd phase4\docker" -ForegroundColor White
Write-Host "  docker-compose down" -ForegroundColor White
Write-Host "  docker-compose up -d" -ForegroundColor White

Write-Host "`n✅ Migration template created!`n" -ForegroundColor Green
