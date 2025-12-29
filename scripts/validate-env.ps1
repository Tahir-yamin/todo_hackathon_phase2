Write-Host "`n Validating Environment Variables...`n" -ForegroundColor Cyan

$envFile = "phase2\frontend\.env.local"
if (Test-Path $envFile) {
    Get-Content $envFile | ForEach-Object {
        if ($_ -match '^([^=]+)=(.*)$') {
            $name = $matches[1].Trim()
            $value = $matches[2].Trim()
            [Environment]::SetEnvironmentVariable($name, $value, "Process")
        }
    }
}

$required = @("DATABASE_URL", "BETTER_AUTH_SECRET", "BETTER_AUTH_URL", "NEXT_PUBLIC_API_URL", "TRUSTED_ORIGINS")
$missing = @()

foreach ($var in $required) {
    $value = [Environment]::GetEnvironmentVariable($var)
    if ([string]::IsNullOrEmpty($value)) {
        $missing += $var
        Write-Host " Missing: $var" -ForegroundColor Red
    } else {
        Write-Host " Found: $var" -ForegroundColor Green
    }
}

Write-Host ""

if ($missing.Count -gt 0) {
    Write-Host " ERROR: Missing required environment variables!" -ForegroundColor Red
    Write-Host "Please set them in phase2\frontend\.env.local" -ForegroundColor Yellow
    exit 1
}

Write-Host " All required environment variables are set!`n" -ForegroundColor Green
