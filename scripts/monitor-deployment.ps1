# ========================================
# Continuous Deployment Monitor
# ========================================
# Monitors GitHub Actions and Pod status
# Auto-resolves common issues
# ========================================

param(
    [int]$IntervalSeconds = 30,
    [int]$MaxChecks = 20
)

$namespace = "todo-chatbot"
$checkCount = 0

Write-Host "🚀 Starting deployment monitor..." -ForegroundColor Green
Write-Host "Namespace: $namespace" -ForegroundColor Yellow
Write-Host "Check interval: $IntervalSeconds seconds" -ForegroundColor Yellow
Write-Host "Max checks: $MaxChecks"
Write-Host "`n$('='*60)`n"

while ($checkCount -lt $MaxChecks) {
    $checkCount++
    $timestamp = Get-Date -Format "HH:mm:ss"
    
    Write-Host "[$timestamp] Check #$checkCount/$MaxChecks" -ForegroundColor Cyan
    
    # ==================== POD STATUS ====================
    Write-Host "`n📦 Pod Status:" -ForegroundColor Yellow
    $pods = kubectl get pods -n $namespace -o json | ConvertFrom-Json
    
    $allHealthy = $true
    foreach ($pod in $pods.items) {
        $name = $pod.metadata.name
        $phase = $pod.status.phase
        
        # Check if pod is healthy
        $isHealthy = $phase -eq "Running"
        if ($pod.status.containerStatuses) {
            foreach ($container in $pod.status.containerStatuses) {
                if (-not $container.ready) {
                    $isHealthy = $false
                }
            }
        }
        
        if ($isHealthy) {
            Write-Host "  ✅ $name - $phase" -ForegroundColor Green
        } else {
            Write-Host "  ❌ $name - $phase" -ForegroundColor Red
            $allHealthy = $false
            
            # Check for common issues
            if ($phase -eq "Pending") {
                Write-Host "    🔍 Checking pending reason..." -ForegroundColor Yellow
                $events = kubectl describe pod $name -n $namespace | Select-String "Events:" -Context 0,5
                Write-Host $events
                
                # Auto-fix: If CPU issue, scale down notification
                if ($events -match "Insufficient cpu") {
                    Write-Host "    🔧 AUTO-FIX: Scaling down notification service" -ForegroundColor Cyan
                    kubectl scale deployment todo-chatbot-notification --replicas=0 -n $namespace 2>$null
                }
            }
            
            if ($phase -eq "CrashLoopBackOff") {
                Write-Host "    🔍 Checking crash logs..." -ForegroundColor Yellow
                kubectl logs $name -n $namespace --tail=20 2>$null
            }
        }
    }
    
    # ==================== DEPLOYMENT STATUS ====================
    Write-Host "`n🚢 Deployment Status:" -ForegroundColor Yellow
    $deployments = kubectl get deployment -n $namespace -o json | ConvertFrom-Json
    
    foreach ($deploy in $deployments.items) {
        $name = $deploy.metadata.name
        $ready = $deploy.status.readyReplicas
        $desired = $deploy.spec.replicas
        
        if ($ready -eq $desired) {
            Write-Host "  ✅ $name - $ready/$desired ready" -ForegroundColor Green
        } else {
            Write-Host "  ⏳ $name - $ready/$desired ready (waiting...)" -ForegroundColor Yellow
        }
    }
    
    # ==================== IMAGE VERSIONS ====================
    Write-Host "`n🏷️  Image Versions:" -ForegroundColor Yellow
    $backendImage = kubectl get deployment todo-chatbot-backend -n $namespace -o jsonpath='{.spec.template.spec.containers[0].image}' 2>$null
    $frontendImage = kubectl get deployment todo-chatbot-frontend -n $namespace -o jsonpath='{.spec.template.spec.containers[0].image}' 2>$null
    
    Write-Host "  Backend:  $backendImage"
    Write-Host "  Frontend: $frontendImage"
    
    # Check if image matches latest commit
    $latestCommit = git log -1 --format="%h" 2>$null
    if ($backendImage -match $latestCommit) {
        Write-Host "  ✅ Backend image is up-to-date ($latestCommit)" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  Backend image may be outdated (latest commit: $latestCommit)" -ForegroundColor Yellow
    }
    
    # ==================== HEALTH CHECK ====================
    if ($allHealthy) {
        Write-Host "`n✅ All pods healthy! Testing backend..." -ForegroundColor Green
        
        # Port-forward and test
        $job = Start-Job -ScriptBlock {
            kubectl port-forward -n todo-chatbot deployment/todo-chatbot-backend 8001:8000 2>$null
        }
        Start-Sleep -Seconds 3
        
        try {
            $health = Invoke-RestMethod -Uri "http://localhost:8001/health" -TimeoutSec 5 -ErrorAction Stop
            if ($health.status -eq "healthy") {
                Write-Host "✅ Backend health check PASSED" -ForegroundColor Green
                Write-Host "`n🎉 DEPLOYMENT SUCCESSFUL!" -ForegroundColor Green
                Write-Host "Application ready at: http://128.203.86.119:3000" -ForegroundColor Cyan
                Stop-Job $job -ErrorAction SilentlyContinue
                Remove-Job $job -ErrorAction SilentlyContinue
                exit 0
            }
        } catch {
            Write-Host "⚠️  Health check failed (pod may still be starting)" -ForegroundColor Yellow
        } finally {
            Stop-Job $job -ErrorAction SilentlyContinue
            Remove-Job $job -ErrorAction SilentlyContinue
        }
    }
    
    Write-Host "`n$('='*60)`n"
    
    if ($checkCount -lt $MaxChecks) {
        Write-Host "⏳ Waiting $IntervalSeconds seconds before next check...`n" -ForegroundColor Gray
        Start-Sleep -Seconds $IntervalSeconds
    }
}

if ($checkCount -eq $MaxChecks) {
    Write-Host "⚠️  Reached maximum checks ($MaxChecks)" -ForegroundColor Yellow
    Write-Host "Deployment may still be in progress." -ForegroundColor Yellow
    Write-Host "`nCheck manually:" -ForegroundColor Cyan
    Write-Host "  kubectl get pods -n $namespace" -ForegroundColor White
    Write-Host "  kubectl logs -l app=backend -n $namespace" -ForegroundColor White
    exit 1
}
