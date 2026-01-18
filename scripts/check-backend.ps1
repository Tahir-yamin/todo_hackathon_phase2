# Check Backend Pod Status

Write-Host "=== BACKEND POD STATUS ===" -ForegroundColor Cyan
kubectl get pods -n todo-chatbot -l app=backend

Write-Host "`n=== BACKEND LOGS (Check for errors) ===" -ForegroundColor Yellow
kubectl logs -l app=backend -n todo-chatbot -c backend --tail=50

Write-Host "`n=== BACKEND DESCRIBE (Check readiness) ===" -ForegroundColor Cyan
kubectl describe pod -l app=backend -n todo-chatbot | Select-String -Pattern "Ready|State|Events" -Context 2,2

Write-Host "`n=== TEST BACKEND DIRECTLY ===" -ForegroundColor Yellow
Write-Host "Testing backend LoadBalancer..." -ForegroundColor White
try {
    $response = Invoke-WebRequest -Uri "http://134.33.248.45:8000/health" -TimeoutSec 5 -UseBasicParsing
    Write-Host "✅ Backend health: $($response.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend not responding: $($_.Exception.Message)" -ForegroundColor Red
}
