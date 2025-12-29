# ===============================================
# AIOps Infrastructure Verification Checklist
# ===============================================
# Verifies that the Kubernetes cluster is fully
# operational with all required features
# ===============================================

Write-Host "🔍 AIOps Infrastructure Verification" -ForegroundColor Cyan
Write-Host ("=" * 50) -ForegroundColor Gray

$allChecksPassed = $true

# ========== CHECK 1: Minikube Status ==========
Write-Host "`n[ ] CHECK 1: Minikube Cluster Status" -ForegroundColor Yellow

try {
    $minikubeStatus = minikube status 2>&1
    
    if ($minikubeStatus -match "Running") {
        Write-Host "[✅] Minikube is running" -ForegroundColor Green
        
        # Get IP
        $minikubeIP = minikube ip
        Write-Host "   Cluster IP: $minikubeIP" -ForegroundColor Gray
    }
    else {
        Write-Host "[❌] Minikube is not running" -ForegroundColor Red
        Write-Host "   Fix: Run .\2-start-minikube.ps1" -ForegroundColor Yellow
        $allChecksPassed = $false
    }
}
catch {
    Write-Host "[❌] Minikube not found or not started" -ForegroundColor Red
    $allChecksPassed = $false
}

# ========== CHECK 2: kubectl Context ==========
Write-Host "`n[ ] CHECK 2: kubectl Context" -ForegroundColor Yellow

try {
    $currentContext = kubectl config current-context
    
    if ($currentContext -eq "minikube") {
        Write-Host "[✅] Context is set to minikube" -ForegroundColor Green
    }
    else {
        Write-Host "[⚠️ ] Context is '$currentContext', should be 'minikube'" -ForegroundColor Yellow
        Write-Host "   Fix: kubectl config use-context minikube" -ForegroundColor Gray
    }
}
catch {
    Write-Host "[❌] kubectl not configured" -ForegroundColor Red
    $allChecksPassed = $false
}

# ========== CHECK 3: Ingress Controller ==========
Write-Host "`n[ ] CHECK 3: Ingress Controller (Nginx)" -ForegroundColor Yellow

try {
    $ingressPods = kubectl get pods -n ingress-nginx -l app.kubernetes.io/component=controller 2>&1
    
    if ($ingressPods -match "Running") {
        Write-Host "[✅] Ingress controller is running" -ForegroundColor Green
        
        # Get pod name
        $podName = ($ingressPods -split "`n" | Select-String "controller" | Select-Object -First 1) -replace "\s+.*", ""
        Write-Host "   Pod: $podName" -ForegroundColor Gray
    }
    else {
        Write-Host "[❌] Ingress controller not running" -ForegroundColor Red
        Write-Host "   Fix: minikube addons enable ingress" -ForegroundColor Yellow
        $allChecksPassed = $false
    }
}
catch {
    Write-Host "[❌] Ingress controller not found" -ForegroundColor Red
    Write-Host "   Fix: minikube addons enable ingress" -ForegroundColor Yellow
    $allChecksPassed = $false
}

# ========== CHECK 4: Metrics Server ==========
Write-Host "`n[ ] CHECK 4: Metrics Server" -ForegroundColor Yellow

try {
    # Try kubectl top nodes
    $metricsOutput = kubectl top nodes 2>&1
    
    if ($metricsOutput -match "CPU" -and $metricsOutput -match "MEMORY") {
        Write-Host "[✅] Metrics server is operational" -ForegroundColor Green
        
        # Show actual metrics
        $metrics = $metricsOutput -split "`n" | Select-Object -Skip 1
        foreach ($line in $metrics) {
            if ($line.Trim()) {
                Write-Host "   $line" -ForegroundColor Gray
            }
        }
    }
    else {
        Write-Host "[❌] Metrics server not responding" -ForegroundColor Red
        Write-Host "   Fix: minikube addons enable metrics-server" -ForegroundColor Yellow
        Write-Host "   Note: May take 30-60 seconds to initialize" -ForegroundColor Gray
        $allChecksPassed = $false
    }
}
catch {
    Write-Host "[❌] Metrics server error" -ForegroundColor Red
    $allChecksPassed = $false
}

# ========== CHECK 5: Dashboard ==========
Write-Host "`n[ ] CHECK 5: Kubernetes Dashboard" -ForegroundColor Yellow

try {
    $dashboardPod = kubectl get pods -n kubernetes-dashboard 2>&1 | Select-String "dashboard"
    
    if ($dashboardPod -match "Running") {
        Write-Host "[✅] Dashboard is running" -ForegroundColor Green
        Write-Host "   Access: minikube dashboard" -ForegroundColor Gray
    }
    else {
        Write-Host "[⚠️ ] Dashboard not running (optional)" -ForegroundColor Yellow
        Write-Host "   Fix: minikube addons enable dashboard" -ForegroundColor Gray
    }
}
catch {
    Write-Host "[⚠️ ] Dashboard not found (optional)" -ForegroundColor Yellow
}

# ========== CHECK 6: Core DNS ==========
Write-Host "`n[ ] CHECK 6: CoreDNS (Cluster DNS)" -ForegroundColor Yellow

try {
    $coreDNS = kubectl get pods -n kube-system -l k8s-app=kube-dns 2>&1
    
    if ($coreDNS -match "Running") {
        Write-Host "[✅] CoreDNS is running" -ForegroundColor Green
    }
    else {
        Write-Host "[⚠️ ] CoreDNS not running (cluster may not resolve services)" -ForegroundColor Yellow
        $allChecksPassed = $false
    }
}
catch {
    Write-Host "[⚠️ ] Could not verify CoreDNS" -ForegroundColor Yellow
}

# ========== CHECK 7: Storage Class ==========
Write-Host "`n[ ] CHECK 7: Storage Class (for PVCs)" -ForegroundColor Yellow

try {
    $storageClass = kubectl get storageclass 2>&1 | Select-String "standard"
    
    if ($storageClass) {
        Write-Host "[✅] Default storage class available" -ForegroundColor Green
    }
    else {
        Write-Host "[⚠️ ] No storage class found" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "[⚠️ ] Could not verify storage class" -ForegroundColor Yellow
}

# ========== CHECK 8: Available Resources ==========
Write-Host "`n[ ] CHECK 8: Cluster Resources" -ForegroundColor Yellow

try {
    # Get node resources if metrics server works
    $nodeInfo = kubectl get nodes -o wide 2>&1 | Select-Object -Skip 1
    
    Write-Host "   $nodeInfo" -ForegroundColor Gray
}
catch {
    Write-Host "[⚠️ ] Could not retrieve node information" -ForegroundColor Yellow
}

# ========== ADDON STATUS SUMMARY ==========
Write-Host "`n📋 Addon Status:" -ForegroundColor Cyan

try {
    $addons = minikube addons list 2>&1 | Select-String "ingress|metrics-server|dashboard"
    
    foreach ($addon in $addons) {
        if ($addon -match "enabled") {
            $addonName = ($addon -split "\|")[0].Trim()
            Write-Host "   ✅ $addonName" -ForegroundColor Green
        }
    }
}
catch {
    Write-Host "   ⚠️  Could not retrieve addon status" -ForegroundColor Yellow
}

# ========== FINAL SUMMARY ==========
Write-Host "`n" + ("=" * 50) -ForegroundColor Cyan

if ($allChecksPassed) {
    Write-Host "✅ ALL CRITICAL CHECKS PASSED!" -ForegroundColor Green
    Write-Host "`nYour AIOps infrastructure is ready!" -ForegroundColor White
    Write-Host "`nNext Steps:" -ForegroundColor White
    Write-Host "  1. Build images: .\1-build-images.ps1" -ForegroundColor Gray
    Write-Host "  2. Deploy app: .\deploy-helm.ps1" -ForegroundColor Gray
}
else {
    Write-Host "⚠️  SOME CHECKS FAILED" -ForegroundColor Yellow
    Write-Host "`nReview the warnings above and fix before proceeding." -ForegroundColor White
    Write-Host "`nCommon Fixes:" -ForegroundColor White
    Write-Host "  • Cluster not running: .\2-start-minikube.ps1" -ForegroundColor Gray
    Write-Host "  • Addons disabled: minikube addons enable <addon-name>" -ForegroundColor Gray
    Write-Host "  • Metrics delayed: Wait 30-60 seconds and rerun" -ForegroundColor Gray
}

Write-Host "`nUseful Commands:" -ForegroundColor White
Write-Host "  • View all pods: kubectl get pods -A" -ForegroundColor Gray
Write-Host "  • Check addons: minikube addons list" -ForegroundColor Gray
Write-Host "  • Dashboard: minikube dashboard" -ForegroundColor Gray
Write-Host "  • Metrics: kubectl top nodes" -ForegroundColor Gray
Write-Host ""
