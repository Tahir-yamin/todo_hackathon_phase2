# ===============================================
# Minikube Setup and Deployment Guide
# ===============================================
# This script sets up Minikube and deploys the todo-chatbot application
# Run each section in PowerShell
# ===============================================

# ========== STEP 1: Start Minikube ==========
# Allocate resources for AI workloads and multi-service deployment

Write-Host "🚀 Starting Minikube with optimal resources..." -ForegroundColor Cyan
minikube start --cpus=4 --memory=4096 --driver=docker

# Verify Minikube is running
Write-Host "`n✅ Verifying Minikube status..." -ForegroundColor Green
minikube status

# ========== STEP 2: Configure Docker Environment ==========
# Point Docker CLI to Minikube's internal registry
# This prevents pushing images to Docker Hub

Write-Host "`n🔧 Configuring Docker to use Minikube registry..." -ForegroundColor Cyan
& minikube -p minikube docker-env --shell powershell | Invoke-Expression

Write-Host "✅ Docker environment configured" -ForegroundColor Green
Write-Host "   All docker build commands now target Minikube's registry" -ForegroundColor Gray

# ========== STEP 3: Build Images in Minikube ==========
# Build images directly into the cluster

Write-Host "`n🏗️  Building images in Minikube registry..." -ForegroundColor Cyan

# Navigate to project root
Set-Location "D:\Hackathon phase 1 TODO App\todo_hackathon_phase1"

# Build Frontend
Write-Host "`n📦 Building Frontend image..." -ForegroundColor Yellow
docker build -t todo-frontend:v1 -f phase4/docker/frontend.Dockerfile .

# Build Backend
Write-Host "`n📦 Building Backend image..." -ForegroundColor Yellow
docker build -t todo-backend:v1 -f phase4/docker/backend.Dockerfile .

# Verify images
Write-Host "`n✅ Verifying images built successfully..." -ForegroundColor Green
docker images | Select-String "todo-"

# ========== STEP 4: Deploy Infrastructure ==========
# Apply namespace, ConfigMap, and Secrets

Write-Host "`n🏗️  Deploying infrastructure layer..." -ForegroundColor Cyan

# Apply namespace and config
kubectl apply -f phase4/k8s/infrastructure.yaml

# Apply secrets
kubectl apply -f phase4/k8s/secrets.yaml

# Verify infrastructure
Write-Host "`n✅ Verifying infrastructure..." -ForegroundColor Green
kubectl get ns | Select-String "todo-chatbot"
kubectl get configmap -n todo-chatbot
kubectl get secrets -n todo-chatbot

# ========== STEP 5: Deploy Database ==========
# Deploy PostgreSQL with persistent storage

Write-Host "`n💾 Deploying PostgreSQL database..." -ForegroundColor Cyan
kubectl apply -f phase4/k8s/database.yaml

# Wait for database to be ready
Write-Host "`n⏳ Waiting for database to be ready..." -ForegroundColor Yellow
kubectl wait --for=condition=ready pod -l app=postgres -n todo-chatbot --timeout=120s

# Verify database
Write-Host "`n✅ Database deployed successfully!" -ForegroundColor Green
kubectl get pods -n todo-chatbot
kubectl get pvc -n todo-chatbot

# ========== STEP 6: Initialize Database Schema ==========
# Port-forward and run Prisma migrations

Write-Host "`n🔄 Setting up database schema..." -ForegroundColor Cyan
Write-Host "   Starting port-forward to database..." -ForegroundColor Gray

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
    Write-Host "`n⚠️  Prisma migration failed. You may need to run it manually." -ForegroundColor Yellow
    Write-Host "   Command: npx prisma db push" -ForegroundColor Gray
}

# Stop port-forward
Stop-Job -Job $portForwardJob
Remove-Job -Job $portForwardJob

# Return to project root
Set-Location "..\.."

# ========== STEP 7: Deploy Application Services ==========
# Deploy Frontend and Backend

Write-Host "`n🚀 Deploying application services..." -ForegroundColor Cyan
kubectl apply -f phase4/k8s/app-deployments.yaml

# Wait for deployments to be ready
Write-Host "`n⏳ Waiting for application pods to be ready..." -ForegroundColor Yellow

kubectl wait --for=condition=available deployment/backend-deployment -n todo-chatbot --timeout=180s
kubectl wait --for=condition=available deployment/frontend-deployment -n todo-chatbot --timeout=180s

Write-Host "`n✅ Application deployed successfully!" -ForegroundColor Green

# Show all pods
Write-Host "`n📊 Current Pod Status:" -ForegroundColor Cyan
kubectl get pods -n todo-chatbot

# ========== STEP 8: Access the Application ==========
Write-Host "`n🌐 Getting application URL..." -ForegroundColor Cyan

# Get Minikube IP and NodePort details
$minikubeIP = minikube ip
$nodePort = 30000

Write-Host "`n✅ Application is accessible at:" -ForegroundColor Green
Write-Host "   Frontend: http://$minikubeIP`:$nodePort" -ForegroundColor White
Write-Host "   Or use: minikube service frontend-service -n todo-chatbot --url" -ForegroundColor Gray

# ========== STEP 9: Summary ==========
Write-Host "`n" + ("=" * 50) -ForegroundColor Cyan
Write-Host "🎉 Complete Stack Deployed to Minikube!" -ForegroundColor Green
Write-Host ("=" * 50) -ForegroundColor Cyan

Write-Host "`nDeployed Resources:" -ForegroundColor White
Write-Host "  ✅ Namespace: todo-chatbot" -ForegroundColor Gray
Write-Host "  ✅ ConfigMap: todo-config" -ForegroundColor Gray
Write-Host "  ✅ Secrets: todo-secrets" -ForegroundColor Gray
Write-Host "  ✅ Database: PostgreSQL 15 (StatefulSet)" -ForegroundColor Gray
Write-Host "  ✅ Storage: 1Gi PersistentVolume" -ForegroundColor Gray
Write-Host "  ✅ Backend: FastAPI (1 replica)" -ForegroundColor Gray
Write-Host "  ✅ Frontend: Next.js (2 replicas)" -ForegroundColor Gray

Write-Host "`nApplication Access:" -ForegroundColor White
Write-Host "  🌐 Frontend: http://$minikubeIP`:30000" -ForegroundColor Cyan
Write-Host "  🔧 Backend API: Accessible via frontend (internal)" -ForegroundColor Gray
Write-Host "  💾 Database: Internal only (db-service:5432)" -ForegroundColor Gray

Write-Host "`nAgent Tools Available:" -ForegroundColor White
Write-Host "  • k8s_cluster_status - View all pod status" -ForegroundColor Gray
Write-Host "  • scale_deployment - Scale frontend/backend" -ForegroundColor Gray  
Write-Host "  • restart_deployment - Rolling restart" -ForegroundColor Gray
Write-Host "  • analyze_pod_logs - Debug pod issues" -ForegroundColor Gray
Write-Host "  • check_pvc_storage - Monitor database storage" -ForegroundColor Gray

Write-Host "`nUseful Commands:" -ForegroundColor White
Write-Host "  • View all resources: kubectl get all -n todo-chatbot" -ForegroundColor Gray
Write-Host "  • View logs: kubectl logs -f <pod-name> -n todo-chatbot" -ForegroundColor Gray
Write-Host "  • Access dashboard: minikube dashboard" -ForegroundColor Gray
Write-Host "  • Open frontend: minikube service frontend-service -n todo-chatbot" -ForegroundColor Gray
Write-Host "  • Stop Minikube: minikube stop" -ForegroundColor Gray
Write-Host ""
