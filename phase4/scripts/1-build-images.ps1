# ===============================================
# Docker-Agent: Autonomous Build Sequence (PowerShell)
# ===============================================
# This script implements the Agentic Protocol:
# 1. Verifies Prisma binary targets
# 2. Builds multi-stage Docker images
# 3. Injects images into Minikube registry
# ===============================================

$ErrorActionPreference = "Stop"

# --- CONFIGURATION ---
$FRONTEND_IMAGE = "todo-frontend"
$BACKEND_IMAGE = "todo-backend"
$TAG = "v1"
$PROJECT_ROOT = (Get-Item ..).Parent.FullName

Write-Host "🚀 [DOCKER-AGENT] Starting autonomous build sequence..." -ForegroundColor Cyan
Write-Host "📍 Project root: $PROJECT_ROOT" -ForegroundColor Gray

# ========== STEP 1: Prisma Binary Sync ==========
Write-Host "`n📂 Step 1: Synchronizing Prisma binary targets..." -ForegroundColor Cyan

Set-Location "$PROJECT_ROOT\phase2\frontend"

# Check if schema.prisma has the correct binary targets
$schemaContent = Get-Content "prisma\schema.prisma" -Raw

if ($schemaContent -notmatch "linux-musl-openssl-3.0.x") {
    Write-Host "⚠️  Missing linux-musl target. Auto-fixing schema.prisma..." -ForegroundColor Yellow
    
    # Backup original
    Copy-Item "prisma\schema.prisma" "prisma\schema.prisma.backup"
    
    # Update binaryTargets
    $schemaContent = $schemaContent -replace 'binaryTargets = \["native"\]', 'binaryTargets = ["native", "linux-musl-openssl-3.0.x"]'
    $schemaContent = $schemaContent -replace 'binaryTargets = \[(.+?)\]', 'binaryTargets = [$1, "linux-musl-openssl-3.0.x"]'
    
    Set-Content "prisma\schema.prisma" $schemaContent
    
    Write-Host "✅ Binary targets updated" -ForegroundColor Green
}
else {
    Write-Host "✅ Prisma schema already has linux-musl target" -ForegroundColor Green
}

# Generate Prisma client locally (for verification)
Write-Host "🔧 Generating Prisma client..." -ForegroundColor Gray
npx prisma generate

Set-Location "$PROJECT_ROOT\phase4\scripts"

# ========== STEP 2: Build Frontend ==========
Write-Host "`n🌐 Step 2: Building Frontend (Next.js Standalone)..." -ForegroundColor Cyan
Write-Host "   Image: ${FRONTEND_IMAGE}:${TAG}" -ForegroundColor Gray

docker build `
    -t "${FRONTEND_IMAGE}:${TAG}" `
    -f "$PROJECT_ROOT\phase4\docker\frontend.Dockerfile" `
    "$PROJECT_ROOT"

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Frontend image built successfully" -ForegroundColor Green
}
else {
    Write-Host "❌ Frontend build failed!" -ForegroundColor Red
    exit 1
}

# ========== STEP 3: Build Backend ==========
Write-Host "`n🐍 Step 3: Building Backend (FastAPI)..." -ForegroundColor Cyan
Write-Host "   Image: ${BACKEND_IMAGE}:${TAG}" -ForegroundColor Gray

docker build `
    -t "${BACKEND_IMAGE}:${TAG}" `
    -f "$PROJECT_ROOT\phase4\docker\backend.Dockerfile" `
    "$PROJECT_ROOT"

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Backend image built successfully" -ForegroundColor Green
}
else {
    Write-Host "❌ Backend build failed!" -ForegroundColor Red
    exit 1
}

# ========== STEP 4: Minikube Image Injection ==========
Write-Host "`n📥 Step 4: Loading images into Minikube cluster..." -ForegroundColor Cyan

# Check if Minikube is running
minikube status 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Minikube is not running. Starting Minikube..." -ForegroundColor Yellow
    minikube start --cpus=4 --memory=4096 --driver=docker
}

Write-Host "   Loading frontend image..." -ForegroundColor Gray
minikube image load "${FRONTEND_IMAGE}:${TAG}"

Write-Host "   Loading backend image..." -ForegroundColor Gray
minikube image load "${BACKEND_IMAGE}:${TAG}"

Write-Host "✅ Images loaded into Minikube" -ForegroundColor Green

# ========== STEP 5: Verification ==========
Write-Host "`n🔍 Step 5: Verifying images..." -ForegroundColor Cyan

# Get image sizes
$frontendSize = (docker images "${FRONTEND_IMAGE}:${TAG}" --format "{{.Size}}").Trim()
$backendSize = (docker images "${BACKEND_IMAGE}:${TAG}" --format "{{.Size}}").Trim()

Write-Host "   Frontend size: $frontendSize" -ForegroundColor Gray
Write-Host "   Backend size: $backendSize" -ForegroundColor Gray

# Verify images in Minikube
Write-Host "`n   Verifying images in Minikube..." -ForegroundColor Gray
$minikubeImages = minikube image ls | Select-String "todo-"
if ($minikubeImages) {
    Write-Host "   ✅ Images found in Minikube:" -ForegroundColor Green
    $minikubeImages | ForEach-Object { Write-Host "      $_" -ForegroundColor Gray }
}
else {
    Write-Host "   ⚠️  Warning: Images not found in Minikube" -ForegroundColor Yellow
}

# ========== SUMMARY ==========
Write-Host "`n" + ("=" * 50) -ForegroundColor Cyan
Write-Host "✅ [SUCCESS] Build sequence complete!" -ForegroundColor Green
Write-Host ("=" * 50) -ForegroundColor Cyan

Write-Host "`nBuilt Images:" -ForegroundColor White
Write-Host "  • ${FRONTEND_IMAGE}:${TAG} - $frontendSize" -ForegroundColor Gray
Write-Host "  • ${BACKEND_IMAGE}:${TAG} - $backendSize" -ForegroundColor Gray

Write-Host "`nNext Steps:" -ForegroundColor White
Write-Host "  1. Deploy with Helm: .\deploy-helm.ps1" -ForegroundColor Gray
Write-Host "  2. Or use kubectl: kubectl apply -f ..\k8s\" -ForegroundColor Gray
Write-Host ""
