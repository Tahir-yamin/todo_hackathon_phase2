# Optimized Frontend Build & Deploy Script
# Uses Docker BuildKit caching for 5-10x faster builds

param(
    [string]$Tag = "chat-fix-$(Get-Date -Format 'yyyyMMddHHmmss')"
)

Write-Host "🚀 Starting Optimized Frontend Build" -ForegroundColor Cyan
Write-Host "Tag: $Tag" -ForegroundColor Yellow

# Enable Docker BuildKit for caching
$env:DOCKER_BUILDKIT = 1
$env:BUILDKIT_PROGRESS = "plain"

# Build with optimized Dockerfile
Write-Host "`n📦 Building Docker image with npm ci + caching..." -ForegroundColor Cyan
docker build `
    --build-arg BUILDKIT_INLINE_CACHE=1 `
    -t "todo-frontend:$Tag" `
    -f phase4/docker/frontend-optimized.Dockerfile `
    .

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker build failed!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Docker build complete!" -ForegroundColor Green

# Tag for ACR
Write-Host "`n🏷️  Tagging image for ACR..." -ForegroundColor Cyan
docker tag "todo-frontend:$Tag" "tahirtodo123.azurecr.io/todo-frontend:$Tag"

# Login to ACR
Write-Host "`n🔐 Logging into Azure Container Registry..." -ForegroundColor Cyan
az acr login --name tahirtodo123

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ ACR login failed!" -ForegroundColor Red
    exit 1
}

# Push to ACR
Write-Host "`n⬆️  Pushing image to ACR..." -ForegroundColor Cyan
docker push "tahirtodo123.azurecr.io/todo-frontend:$Tag"

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker push failed!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Image pushed to ACR!" -ForegroundColor Green

# Update Kubernetes deployment
Write-Host "`n🚢 Updating Kubernetes deployment..." -ForegroundColor Cyan
kubectl set image deployment/todo-chatbot-frontend `
    frontend="tahirtodo123.azurecr.io/todo-frontend:$Tag" `
    -n todo-chatbot

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Kubernetes update failed!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Deployment updated!" -ForegroundColor Green

# Wait for rollout
Write-Host "`n⏳ Waiting for rollout to complete..." -ForegroundColor Cyan
kubectl rollout status deployment/todo-chatbot-frontend -n todo-chatbot --timeout=5m

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Rollout failed or timed out!" -ForegroundColor Red
    exit 1
}

Write-Host "`n🎉 Frontend deployed successfully with chat widget fix!" -ForegroundColor Green
Write-Host "Image: tahirtodo123.azurecr.io/todo-frontend:$Tag" -ForegroundColor Yellow
Write-Host "Access: http://128.203.86.119:3000" -ForegroundColor Cyan
