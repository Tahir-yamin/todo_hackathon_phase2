# ===============================================
# Helm-Based Deployment for Evolution Todo
# ===============================================
# This script deploys the application using Helm
# instead of raw kubectl apply commands.
# ===============================================

Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "Evolution Todo - Helm Deployment" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Cyan

# ========== STEP 1: Start Minikube ==========
Write-Host "`n🚀 Starting Minikube..." -ForegroundColor Cyan

minikube start --cpus=4 --memory=4096 --driver=docker

# Verify Minikube is running
Write-Host "`n✅ Minikube status:" -ForegroundColor Green
minikube status

# ========== STEP 2: Configure Docker Environment ==========
Write-Host "`n🔧 Configuring Docker to use Minikube registry..." -ForegroundColor Cyan
& minikube -p minikube docker-env --shell powershell | Invoke-Expression

Write-Host "✅ Docker environment configured" -ForegroundColor Green

# ========== STEP 3: Build Images ==========
Write-Host "`n🏗️  Building images..." -ForegroundColor Cyan

# Navigate to project root
Set-Location "D:\Hackathon phase 1 TODO App\todo_hackathon_phase1"

# Build Frontend
Write-Host "`n📦 Building Frontend (todo-frontend:v1)..." -ForegroundColor Yellow
docker build -t todo-frontend:v1 -f phase4/docker/frontend.Dockerfile .

# Build Backend
Write-Host "`n📦 Building Backend (todo-backend:v1)..." -ForegroundColor Yellow
docker build -t todo-backend:v1 -f phase4/docker/backend.Dockerfile .

# Verify images
Write-Host "`n✅ Images built successfully:" -ForegroundColor Green
docker images | Select-String "todo-"

# ========== STEP 4: Deploy with Helm ==========
Write-Host "`n📦 Deploying with Helm..." -ForegroundColor Cyan

# Install or upgrade the release
helm upgrade --install evolution-todo ./phase4/helm/todo-chatbot `
    --namespace todo-chatbot `
    --create-namespace `
    --wait `
    --timeout 5m

Write-Host "`n✅ Helm release deployed!" -ForegroundColor Green

# ========== STEP 5: Wait for Pods ==========
Write-Host "`n⏳ Waiting for pods to be ready..." -ForegroundColor Yellow

# Wait for database
kubectl wait --for=condition=ready pod -l app=postgres -n todo-chatbot --timeout=120s

# Wait for backend
kubectl wait --for=condition=available deployment -l app=backend -n todo-chatbot --timeout=180s

# Wait for frontend
kubectl wait --for=condition=available deployment -l app=frontend -n todo-chatbot --timeout=180s

Write-Host "`n✅ All pods are ready!" -ForegroundColor Green

# ========== STEP 6: Initialize Database ==========
Write-Host "`n🔄 Setting up database schema..." -ForegroundColor Cyan

# Start port-forward in background
$portForwardJob = Start-Job -ScriptBlock {
    kubectl port-forward pod/postgres-0 5432:5432 -n todo-chatbot
}

# Wait for port-forward to establish
Start-Sleep -Seconds 5

# Run Prisma migration
Write-Host "`n📊 Running Prisma schema push..." -ForegroundColor Yellow
Set-Location "phase2\frontend"

try {
    npx prisma db push
    Write-Host "`n✅ Database schema initialized!" -ForegroundColor Green
}
catch {
    Write-Host "`n⚠️  Prisma migration failed. Run manually if needed." -ForegroundColor Yellow
    Write-Host "   Command: npx prisma db push" -ForegroundColor Gray
}

# Stop port-forward
Stop-Job -Job $portForwardJob
Remove-Job -Job $portForwardJob

# Return to project root
Set-Location "..\.."

# ========== STEP 7: Get Access URL ==========
Write-Host "`n🌐 Getting application URL..." -ForegroundColor Cyan

$minikubeIP = minikube ip
$nodePort = 30000

Write-Host "`n✅ Application is accessible at:" -ForegroundColor Green
Write-Host "   Frontend: http://$minikubeIP`:$nodePort" -ForegroundColor White
Write-Host "   Or use: minikube service frontend-service -n todo-chatbot" -ForegroundColor Gray

# ========== STEP 8: Display Release Info ==========
Write-Host "`n📋 Helm Release Information:" -ForegroundColor Cyan
helm list -n todo-chatbot

Write-Host "`n📊 Pod Status:" -ForegroundColor Cyan
kubectl get pods -n todo-chatbot

# ========== STEP 9: Summary ==========
Write-Host "`n" + ("=" * 60) -ForegroundColor Cyan
Write-Host "🎉 Helm Deployment Complete!" -ForegroundColor Green
Write-Host ("=" * 60) -ForegroundColor Cyan

Write-Host "`nDeployed Components:" -ForegroundColor White
Write-Host "  ✅ Release: evolution-todo (Helm managed)" -ForegroundColor Gray
Write-Host "  ✅ Namespace: todo-chatbot" -ForegroundColor Gray
Write-Host "  ✅ Database: PostgreSQL 15 (1 replica)" -ForegroundColor Gray
Write-Host "  ✅ Backend: FastAPI (1 replica)" -ForegroundColor Gray
Write-Host "  ✅ Frontend: Next.js (2 replicas)" -ForegroundColor Gray

Write-Host "`nHelm Commands:" -ForegroundColor White
Write-Host "  • List releases: helm list -n todo-chatbot" -ForegroundColor Gray
Write-Host "  • View history: helm history evolution-todo -n todo-chatbot" -ForegroundColor Gray
Write-Host "  • Upgrade: helm upgrade evolution-todo ./phase4/helm/todo-chatbot" -ForegroundColor Gray
Write-Host "  • Rollback: helm rollback evolution-todo -n todo-chatbot" -ForegroundColor Gray
Write-Host "  • Uninstall: helm uninstall evolution-todo -n todo-chatbot" -ForegroundColor Gray

Write-Host "`nAccess Application:" -ForegroundColor White
Write-Host "  🌐 http://$minikubeIP`:30000" -ForegroundColor Cyan

Write-Host "`nKubernetes Commands:" -ForegroundColor White
Write-Host "  • View pods: kubectl get pods -n todo-chatbot" -ForegroundColor Gray
Write-Host "  • View logs: kubectl logs -f <pod-name> -n todo-chatbot" -ForegroundColor Gray
Write-Host "  • Dashboard: minikube dashboard" -ForegroundColor Gray

Write-Host ""
