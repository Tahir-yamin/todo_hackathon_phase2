#!/bin/bash
set -e

# ===============================================
# Docker-Agent: Autonomous Build Sequence
# ===============================================
# This script implements the Agentic Protocol:
# 1. Verifies Prisma binary targets
# 2. Builds multi-stage Docker images
# 3. Injects images into Minikube registry
# ===============================================

# --- CONFIGURATION ---
FRONTEND_IMAGE="todo-frontend"
BACKEND_IMAGE="todo-backend"
TAG="v1"
PROJECT_ROOT="$(cd ../.. && pwd)"

echo "🚀 [DOCKER-AGENT] Starting autonomous build sequence..."
echo "📍 Project root: $PROJECT_ROOT"

# ========== STEP 1: Prisma Binary Sync ==========
echo ""
echo "📂 Step 1: Synchronizing Prisma binary targets..."
cd "$PROJECT_ROOT/phase2/frontend"

# Check if schema.prisma has the correct binary targets
if ! grep -q "linux-musl-openssl-3.0.x" prisma/schema.prisma; then
    echo "⚠️  Missing linux-musl target. Auto-fixing schema.prisma..."
    
    # Backup original
    cp prisma/schema.prisma prisma/schema.prisma.backup
    
    # Inject linux-musl binary target
    sed -i.bak 's/binaryTargets = \[/binaryTargets = ["native", "linux-musl-openssl-3.0.x", /' prisma/schema.prisma
    
    echo "✅ Binary targets updated"
else
    echo "✅ Prisma schema already has linux-musl target"
fi

# Generate Prisma client locally (for verification)
echo "🔧 Generating Prisma client..."
npx prisma generate

cd "$PROJECT_ROOT/phase4/scripts"

# ========== STEP 2: Build Frontend ==========
echo ""
echo "🌐 Step 2: Building Frontend (Next.js Standalone)..."
echo "   Image: ${FRONTEND_IMAGE}:${TAG}"

docker build \
    --progress=plain \
    -t ${FRONTEND_IMAGE}:${TAG} \
    -f "$PROJECT_ROOT/phase4/docker/frontend.Dockerfile" \
    "$PROJECT_ROOT"

echo "✅ Frontend image built successfully"

# ========== STEP 3: Build Backend ==========
echo ""
echo "🐍 Step 3: Building Backend (FastAPI)..."
echo "   Image: ${BACKEND_IMAGE}:${TAG}"

docker build \
    --progress=plain \
    -t ${BACKEND_IMAGE}:${TAG} \
    -f "$PROJECT_ROOT/phase4/docker/backend.Dockerfile" \
    "$PROJECT_ROOT"

echo "✅ Backend image built successfully"

# ========== STEP 4: Minikube Image Injection ==========
echo ""
echo "📥 Step 4: Loading images into Minikube cluster..."

# Check if Minikube is running
if ! minikube status &> /dev/null; then
    echo "⚠️  Minikube is not running. Starting Minikube..."
    minikube start --cpus=4 --memory=4096 --driver=docker
fi

echo "   Loading frontend image..."
minikube image load ${FRONTEND_IMAGE}:${TAG}

echo "   Loading backend image..."
minikube image load ${BACKEND_IMAGE}:${TAG}

echo "✅ Images loaded into Minikube"

# ========== STEP 5: Verification ==========
echo ""
echo "🔍 Step 5: Verifying images..."

# Get image sizes
FRONTEND_SIZE=$(docker images ${FRONTEND_IMAGE}:${TAG} --format "{{.Size}}")
BACKEND_SIZE=$(docker images ${BACKEND_IMAGE}:${TAG} --format "{{.Size}}")

echo "   Frontend size: $FRONTEND_SIZE"
echo "   Backend size: $BACKEND_SIZE"

# Verify images in Minikube
echo ""
echo "   Verifying images in Minikube..."
minikube image ls | grep todo- || echo "⚠️  Warning: Images not found in Minikube"

# ========== SUMMARY ==========
echo ""
echo "=========================================="
echo "✅ [SUCCESS] Build sequence complete!"
echo "=========================================="
echo ""
echo "Built Images:"
echo "  • ${FRONTEND_IMAGE}:${TAG} - $FRONTEND_SIZE"
echo "  • ${BACKEND_IMAGE}:${TAG} - $BACKEND_SIZE"
echo ""
echo "Next Steps:"
echo "  1. Deploy with Helm: cd scripts && ./deploy-helm.ps1"
echo "  2. Or use kubectl: kubectl apply -f ../k8s/"
echo ""
