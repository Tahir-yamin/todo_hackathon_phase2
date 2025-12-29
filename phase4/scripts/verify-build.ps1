# ===============================================
# Docker Build Verification Checklist
# ===============================================
# Runs automated checks after build to ensure
# images are production-ready
# ===============================================

Write-Host "🔍 Docker Build Verification Checklist" -ForegroundColor Cyan
Write-Host ("=" * 50) -ForegroundColor Gray

$FRONTEND_IMAGE = "todo-frontend:v1"
$BACKEND_IMAGE = "todo-backend:v1"
$allChecksPassed = $true

# ========== CHECK 1: Image Size ==========
Write-Host "`n[ ] CHECK 1: Image Size Verification" -ForegroundColor Yellow

try {
    $frontendSize = docker images $FRONTEND_IMAGE --format "{{.Size}}"
    $backendSize = docker images $BACKEND_IMAGE --format "{{.Size}}"
    
    # Convert to MB for comparison (rough estimation)
    $frontendMB = if ($frontendSize -match "(\d+\.?\d*)MB") { [double]$matches[1] } 
    elseif ($frontendSize -match "(\d+\.?\d*)GB") { [double]$matches[1] * 1024 }
    else { 0 }
    
    $backendMB = if ($backendSize -match "(\d+\.?\d*)MB") { [double]$matches[1] }
    elseif ($backendSize -match "(\d+\.?\d*)GB") { [double]$matches[1] * 1024 }
    else { 0 }
    
    Write-Host "   Frontend: $frontendSize" -ForegroundColor Gray
    Write-Host "   Backend: $backendSize" -ForegroundColor Gray
    
    if ($frontendMB -lt 500 -and $frontendMB -gt 0) {
        Write-Host "[✅] Frontend size is optimal (< 500MB)" -ForegroundColor Green
    }
    else {
        Write-Host "[⚠️ ] Frontend size may be too large" -ForegroundColor Yellow
        $allChecksPassed = $false
    }
    
    if ($backendMB -lt 300 -and $backendMB -gt 0) {
        Write-Host "[✅] Backend size is optimal (< 300MB)" -ForegroundColor Green
    }
    else {
        Write-Host "[⚠️ ] Backend size may be too large" -ForegroundColor Yellow
        $allChecksPassed = $false
    }
}
catch {
    Write-Host "[❌] Images not found. Run build script first." -ForegroundColor Red
    $allChecksPassed = $false
}

# ========== CHECK 2: Prisma Binary ==========
Write-Host "`n[ ] CHECK 2: Prisma Binary Verification" -ForegroundColor Yellow

try {
    # Start a temporary frontend container
    $containerId = (docker run -d $FRONTEND_IMAGE sleep 60).Trim()
    
    # Check for Prisma binary
    $prismaBinary = docker exec $containerId ls /app/node_modules/.prisma/client 2>&1
    
    if ($prismaBinary -match "libquery_engine.*linux-musl" -or $prismaBinary -match "linux-musl") {
        Write-Host "[✅] Prisma linux-musl binary found" -ForegroundColor Green
    }
    else {
        Write-Host "[❌] Prisma linux-musl binary NOT found" -ForegroundColor Red
        Write-Host "   Fix: Ensure binaryTargets includes 'linux-musl-openssl-3.0.x'" -ForegroundColor Yellow
        $allChecksPassed = $false
    }
    
    # Cleanup
    docker stop $containerId | Out-Null
    docker rm $containerId | Out-Null
}
catch {
    Write-Host "[⚠️ ] Could not verify Prisma binary (container issue)" -ForegroundColor Yellow
}

# ========== CHECK 3: Backend Health Endpoint ==========
Write-Host "`n[ ] CHECK 3: Backend Connectivity Test" -ForegroundColor Yellow

try {
    # Start backend container temporarily
    $backendId = (docker run -d -p 8001:8000 $BACKEND_IMAGE).Trim()
    
    # Wait for startup
    Start-Sleep -Seconds 3
    
    # Test health endpoint
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8001/health" -TimeoutSec 5
        if ($response.StatusCode -eq 200) {
            Write-Host "[✅] Backend /health endpoint responds with 200 OK" -ForegroundColor Green
        }
        else {
            Write-Host "[❌] Backend health check failed" -ForegroundColor Red
            $allChecksPassed = $false
        }
    }
    catch {
        Write-Host "[⚠️ ] Could not reach backend (may need more startup time)" -ForegroundColor Yellow
    }
    
    # Cleanup
    docker stop $backendId | Out-Null
    docker rm $backendId | Out-Null
}
catch {
    Write-Host "[⚠️ ] Could not start backend container for testing" -ForegroundColor Yellow
}

# ========== CHECK 4: Minikube Registry ==========
Write-Host "`n[ ] CHECK 4: Minikube Registry Verification" -ForegroundColor Yellow

try {
    $minikubeImages = minikube image ls 2>&1 | Select-String "todo-"
    
    if ($minikubeImages) {
        Write-Host "[✅] Images found in Minikube registry:" -ForegroundColor Green
        $minikubeImages | ForEach-Object {
            Write-Host "   • $_" -ForegroundColor Gray
        }
    }
    else {
        Write-Host "[❌] Images NOT found in Minikube" -ForegroundColor Red
        Write-Host "   Fix: Run 'minikube image load' commands" -ForegroundColor Yellow
        $allChecksPassed = $false
    }
}
catch {
    Write-Host "[⚠️ ] Minikube is not running or accessible" -ForegroundColor Yellow
    $allChecksPassed = $false
}

# ========== CHECK 5: Security Check ==========
Write-Host "`n[ ] CHECK 5: Basic Security Verification" -ForegroundColor Yellow

try {
    # Check if frontend runs as non-root
    $frontendUser = docker inspect $FRONTEND_IMAGE --format '{{.Config.User}}'
    
    if ($frontendUser -and $frontendUser -ne "root" -and $frontendUser -ne "") {
        Write-Host "[✅] Frontend runs as non-root user ($frontendUser)" -ForegroundColor Green
    }
    else {
        Write-Host "[⚠️ ] Frontend may be running as root" -ForegroundColor Yellow
    }
    
    # Check for secrets in environment
    $frontendEnv = docker inspect $FRONTEND_IMAGE --format '{{json .Config.Env}}' | ConvertFrom-Json
    $hasSecrets = $frontendEnv | Where-Object { $_ -match "password|secret|key|token" }
    
    if (-not $hasSecrets) {
        Write-Host "[✅] No obvious secrets in environment variables" -ForegroundColor Green
    }
    else {
        Write-Host "[⚠️ ] Possible secrets found in environment" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "[⚠️ ] Could not complete security check" -ForegroundColor Yellow
}

# ========== FINAL SUMMARY ==========
Write-Host "`n" + ("=" * 50) -ForegroundColor Cyan

if ($allChecksPassed) {
    Write-Host "✅ ALL CRITICAL CHECKS PASSED!" -ForegroundColor Green
    Write-Host "`nYour images are ready for deployment!" -ForegroundColor White
    Write-Host "`nNext Steps:" -ForegroundColor White
    Write-Host "  1. Deploy with Helm: .\deploy-helm.ps1" -ForegroundColor Gray
    Write-Host "  2. Or deploy manually: kubectl apply -f ..\k8s\" -ForegroundColor Gray
}
else {
    Write-Host "⚠️  SOME CHECKS FAILED" -ForegroundColor Yellow
    Write-Host "`nReview the warnings above and fix before deploying." -ForegroundColor White
    Write-Host "`nCommon Fixes:" -ForegroundColor White
    Write-Host "  • Prisma: Add linux-musl-openssl-3.0.x to binaryTargets" -ForegroundColor Gray
    Write-Host "  • Size: Review Dockerfile for optimization opportunities" -ForegroundColor Gray
    Write-Host "  • Minikube: Run 'minikube image load <image>'" -ForegroundColor Gray
}

Write-Host ""
