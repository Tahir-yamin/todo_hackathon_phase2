# Fast Backend Build & Deploy with Kafka Integration
cd "d:\Hackathon phase 1 TODO App\todo_hackathon_phase1\phase2\backend"

Write-Host "`n🚀 Building backend with Kafka integration...`n" -ForegroundColor Cyan

# Build backend image
$timestamp = Get-Date -Format "yyyyMMddHHmmss"
$tag = "kafka-$timestamp"

docker build -t todo-backend:$tag .

Write-Host "`n✅ Backend built!`n" -ForegroundColor Green

# Tag for ACR
docker tag todo-backend:$tag tahirtodo123.azurecr.io/todo-backend:$tag

# Push to ACR  
Write-Host "`n📤 Pushing to ACR...`n" -ForegroundColor Cyan
docker push tahirtodo123.azurecr.io/todo-backend:$tag

# Upgrade Helm deployment
Write-Host "`n🔄 Upgrading Helm deployment...`n" -ForegroundColor Cyan
cd "d:\Hackathon phase 1 TODO App\todo_hackathon_phase1\phase4\helm"

helm upgrade todo-chatbot ./todo-chatbot `
  --namespace todo-chatbot `
  --set backend.image.repository=tahirtodo123.azurecr.io/todo-backend `
  --set backend.image.tag=$tag `
  --wait --timeout=5m

# Check deployment
kubectl rollout status deployment/todo-chatbot-backend -n todo-chatbot

Write-Host "`n✅ DEPLOYMENT COMPLETE!`n" -ForegroundColor Green
Write-Host "Backend with Kafka integration is now running!" -ForegroundColor Cyan
Write-Host "Tag: $tag`n" -ForegroundColor Yellow
