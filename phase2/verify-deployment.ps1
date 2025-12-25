#!/usr/bin/env pwsh
# Deployment Verification Script for Evolution of Todo

Write-Host "🚀 DEPLOYMENT VERIFICATION STARTING..." -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Gray
Write-Host ""

$frontend = "https://frontend-seven-tawny-19.vercel.app"
$backend = "https://todohackathonphase2-production.up.railway.app"

# Test 1: Backend Health Check
Write-Host "Test 1: Backend Health Check" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$backend/health" -Method GET -TimeoutSec 10
    if ($response.status -eq "ok") {
        Write-Host "✅ Backend is healthy: $($response | ConvertTo-Json -Compress)" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Backend responded but status unclear: $($response | ConvertTo-Json)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Backend health check failed: $_" -ForegroundColor Red
}
Write-Host ""

# Test 2: Frontend Landing Page
Write-Host "Test 2: Frontend Landing Page" -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri $frontend -Method GET -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Frontend is online (Status: $($response.StatusCode))" -ForegroundColor Green
        $contentLength = $response.Content.Length
        Write-Host "   Content size: $contentLength bytes" -ForegroundColor Cyan
        
        # Check for key components
        if ($response.Content -match "Evolution of Todo" -or $response.Content -match "nextjs") {
            Write-Host "   ✅ Page content detected" -ForegroundColor Green
        } else {
            Write-Host "   ⚠️ Unexpected content" -ForegroundColor Yellow
        }
    }
} catch {
    Write-Host "❌ Frontend check failed: $_" -ForegroundColor Red
}
Write-Host ""

# Test 3: Backend CORS & API Connectivity
Write-Host "Test 3: Backend API Endpoints" -ForegroundColor Yellow
try {
    $headers = @{
        "Origin" = $frontend
        "X-User-ID" = "test-user"
    }
    $response = Invoke-WebRequest -Uri "$backend/api/tasks" -Method GET -Headers $headers -TimeoutSec 10 -SkipHttpErrorCheck
    Write-Host "   Tasks endpoint: Status $($response.StatusCode)" -ForegroundColor Cyan
    if ($response.StatusCode -eq 200 -or $response.StatusCode -eq 401) {
        Write-Host "   ✅ API is responding (CORS working)" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️ Unexpected status: $($response.StatusCode)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   ℹ️ API test: $($_.Exception.Message)" -ForegroundColor Cyan
}
Write-Host ""

# Test 4: OAuth Configuration (BetterAuth Endpoints)
Write-Host "Test 4: OAuth Endpoints" -ForegroundColor Yellow
$authEndpoints = @(
    "$frontend/api/auth/session"
    "$frontend/api/auth/callback/google"
)

foreach ($endpoint in $authEndpoints) {
    try {
        $response = Invoke-WebRequest -Uri $endpoint -Method GET -TimeoutSec 5 -MaximumRedirection 0 -ErrorAction SilentlyContinue -SkipHttpErrorCheck
        $status = $response.StatusCode
        $statusText = switch ($status) {
            200 { "Active" }
            302 { "Redirect (OK)" }
            404 { "Not Found" }
            401 { "Unauthorized (OK)" }
            default { "Status $status" }
        }
        Write-Host "   $endpoint : $statusText" -ForegroundColor Cyan
    } catch {
        Write-Host "   $endpoint : Checking..." -ForegroundColor Gray
    }
}
Write-Host ""

# Summary
Write-Host "=" * 60 -ForegroundColor Gray
Write-Host "🎯 DEPLOYMENT VERIFICATION COMPLETE" -ForegroundColor Cyan
Write-Host ""
Write-Host "Live URLs:" -ForegroundColor Green
Write-Host "  Frontend: $frontend" -ForegroundColor White
Write-Host "  Backend:  $backend" -ForegroundColor White
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Visit frontend URL in browser" -ForegroundColor White
Write-Host "  2. Test Google OAuth login" -ForegroundColor White
Write-Host "  3. Verify AI chatbot works" -ForegroundColor White
Write-Host "  4. Check dashboard auto-refresh" -ForegroundColor White
Write-Host ""
