# Check Deployment Status

Write-Host "=== 1. LATEST GIT COMMITS ===" -ForegroundColor Cyan
git log --oneline -5

Write-Host "`n=== 2. CURRENT DEPLOYED IMAGE TAGS ===" -ForegroundColor Yellow
kubectl get pods -n todo-chatbot -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[0].image}{"\n"}{end}' | Select-String -Pattern "frontend|backend"

Write-Host "`n=== 3. LATEST GITHUB ACTIONS RUN ===" -ForegroundColor Cyan  
gh run list --repo Tahir-yamin/todo_hackathon_phase2 --limit 3

Write-Host "`n=== 4. TRIGGER NEW DEPLOYMENT ===" -ForegroundColor Yellow
Write-Host "Run this command to trigger a new build:"
Write-Host "git commit --allow-empty -m 'trigger rebuild' && git push origin main" -ForegroundColor Green
