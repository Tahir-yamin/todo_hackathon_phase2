# Diagnostic Script - Run This

Write-Host "=== 1. GET BACKEND CONTAINER NAMES ===" -ForegroundColor Cyan
kubectl get pod -l app=backend -n todo-chatbot -o jsonpath='{.items[0].spec.containers[*].name}'
Write-Host "`n"

Write-Host "`n=== 2. GET BACKEND LOGS (ALL CONTAINERS) ===" -ForegroundColor Yellow
kubectl logs todo-chatbot-backend-5f467fbb98-2qf46 -n todo-chatbot --all-containers=true --tail=40

Write-Host "`n=== 3. CHECK SERVICE ENDPOINTS ===" -ForegroundColor Cyan
kubectl get endpoints -n todo-chatbot | Select-String -Pattern "backend"

Write-Host "`n=== 4. DESCRIBE BACKEND SERVICE ===" -ForegroundColor Yellow
kubectl get svc todo-chatbot-backend -n todo-chatbot -o wide

Write-Host "`n=== 5. TEST FROM INSIDE CLUSTER ===" -ForegroundColor Cyan
kubectl exec todo-chatbot-frontend-fdb4885d9-lx8gh -n todo-chatbot -- wget -qO- --timeout=5 http://backend-service:8000/health

Write-Host "`n=== 6. CHECK POD IP AND PORT ===" -ForegroundColor Yellow
kubectl get pod todo-chatbot-backend-5f467fbb98-2qf46 -n todo-chatbot -o jsonpath='{.status.podIP}{"\n"}'
kubectl get pod todo-chatbot-backend-5f467fbb98-2qf46 -n todo-chatbot -o jsonpath='{.spec.containers[*].ports[*].containerPort}{"\n"}'
