# ===============================================
# AIOps-Pilot: Minikube Cluster Initialization
# ===============================================
# Transforms a blank Docker environment into a
# production-ready Kubernetes cluster with:
# - Ingress (Nginx)
# - Metrics Server (observability)
# - Dashboard (visual management)
# ===============================================

$ErrorActionPreference = "Stop"

Write-Host "🎡 [AIOPS-PILOT] Initializing Minikube Cluster..." -ForegroundColor Cyan
Write-Host ""

# ========== STEP 1: Cluster Start ==========
Write-Host "🚀 Step 1: Starting Minikube with optimized resources..." -ForegroundColor Cyan
Write-Host "   CPUs: 4" -ForegroundColor Gray
Write-Host "   Memory: 4096MB" -ForegroundColor Gray
Write-Host "   Driver: Docker" -ForegroundColor Gray
Write-Host "   Kubernetes: v1.28.3" -ForegroundColor Gray

try {
    # Start Minikube with optimal configuration
    minikube start --cpus=4 --memory=4096 --driver=docker --kubernetes-version=v1.28.3

    
    Write-Host "✅ Minikube started successfully" -ForegroundColor Green
}
catch {
    Write-Host "❌ Failed to start Minikube" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Yellow
    exit 1
}

# ========== STEP 2: Enable Addons ==========
Write-Host "`n🔌 Step 2: Enabling critical cluster features..." -ForegroundColor Cyan

# Enable Ingress
Write-Host "   • Ingress (Nginx)..." -ForegroundColor Gray
try {
    minikube addons enable ingress 2>&1 | Out-Null
    Write-Host "     ✅ Enabled" -ForegroundColor Green
}
catch {
    Write-Host "     Already enabled or failed" -ForegroundColor Yellow
}

# Enable Metrics Server
Write-Host "   • Metrics Server (for kubectl top)..." -ForegroundColor Gray
try {
    minikube addons enable metrics-server 2>&1 | Out-Null
    Write-Host "     ✅ Enabled" -ForegroundColor Green
}
catch {
    Write-Host "     Already enabled or failed" -ForegroundColor Yellow
}

# Enable Dashboard
Write-Host "   • Dashboard (visual management)..." -ForegroundColor Gray
try {
    minikube addons enable dashboard 2>&1 | Out-Null
    Write-Host "     ✅ Enabled" -ForegroundColor Green
}
catch {
    Write-Host "     Already enabled or failed" -ForegroundColor Yellow
}

Write-Host "✅ All addons configured" -ForegroundColor Green

# ========== STEP 3: Context Setup ==========
Write-Host "`n🎯 Step 3: Setting kubectl context to minikube..." -ForegroundColor Cyan

try {
    kubectl config use-context minikube | Out-Null
    Write-Host "✅ kubectl context configured" -ForegroundColor Green
}
catch {
    Write-Host "⚠️  Failed to set context" -ForegroundColor Yellow
}

# ========== STEP 4: Verification ==========
Write-Host "`n🔍 Step 4: Verifying cluster health..." -ForegroundColor Cyan

# Wait for core pods to be ready
Write-Host "   Waiting for core services..." -ForegroundColor Gray
Start-Sleep -Seconds 5

# Check ingress controller
try {
    $ingressPods = kubectl get pods -n ingress-nginx -l app.kubernetes.io/component=controller 2>$null
    if ($ingressPods -match "Running") {
        Write-Host "   ✅ Ingress controller: Running" -ForegroundColor Green
    }
    else {
        Write-Host "   ⚠️  Ingress controller: Starting (may take a minute)" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "   ⚠️  Could not verify ingress controller" -ForegroundColor Yellow
}

# Check metrics server
try {
    $metricsDeployment = kubectl get deployment metrics-server -n kube-system 2>$null
    if ($metricsDeployment -match "1/1") {
        Write-Host "   ✅ Metrics server: Running" -ForegroundColor Green
    }
    else {
        Write-Host "   ⚠️  Metrics server: Starting" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "   ⚠️  Could not verify metrics server" -ForegroundColor Yellow
}

# Get cluster info
Write-Host "`n📊 Cluster Information:" -ForegroundColor Cyan

try {
    $minikubeIP = minikube ip
    Write-Host "   Minikube IP: $minikubeIP" -ForegroundColor Gray
}
catch {
    Write-Host "   Minikube IP: Unable to retrieve" -ForegroundColor Yellow
}

try {
    $k8sVersion = (kubectl version --short 2>$null | Select-String "Server Version") -replace "Server Version: ", ""
    Write-Host "   Kubernetes Version: $k8sVersion" -ForegroundColor Gray
}
catch {
    Write-Host "   Kubernetes Version: Unable to retrieve" -ForegroundColor Yellow
}

$currentContext = kubectl config current-context
Write-Host "   Context: $currentContext" -ForegroundColor Gray

# ========== STEP 5: Useful Commands ==========
Write-Host "`n💡 Useful Commands:" -ForegroundColor Cyan
Write-Host "   • Dashboard: minikube dashboard" -ForegroundColor Gray
Write-Host "   • Tunnel (for Ingress): minikube tunnel" -ForegroundColor Gray
Write-Host "   • View metrics: kubectl top nodes" -ForegroundColor Gray
Write-Host "   • Check ingress: kubectl get pods -n ingress-nginx" -ForegroundColor Gray
Write-Host "   • Stop cluster: minikube stop" -ForegroundColor Gray
Write-Host "   • Delete cluster: minikube delete" -ForegroundColor Gray

# ========== SUMMARY ==========
Write-Host "`n" + ("=" * 50) -ForegroundColor Cyan
Write-Host "✅ [SUCCESS] Cluster initialized!" -ForegroundColor Green
Write-Host ("=" * 50) -ForegroundColor Cyan

Write-Host "`nEnabled Features:" -ForegroundColor White
Write-Host "  • Ingress (Nginx) - HTTP/HTTPS routing" -ForegroundColor Gray
Write-Host "  • Metrics Server - Resource monitoring" -ForegroundColor Gray
Write-Host "  • Dashboard - Visual management" -ForegroundColor Gray

Write-Host "`nNext Steps:" -ForegroundColor White
Write-Host "  1. Build images: .\1-build-images.ps1" -ForegroundColor Gray
Write-Host "  2. Deploy app: .\deploy-helm.ps1" -ForegroundColor Gray

Write-Host ""
