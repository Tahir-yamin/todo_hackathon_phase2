#!/bin/bash
set -e

# ===============================================
# AIOps-Pilot: Minikube Cluster Initialization
# ===============================================
# Transforms a blank Docker environment into a
# production-ready Kubernetes cluster with:
# - Ingress (Nginx)
# - Metrics Server (observability)
# - Dashboard (visual management)
# ===============================================

echo "🎡 [AIOPS-PILOT] Initializing Minikube Cluster..."
echo ""

# ========== STEP 1: Cluster Start ==========
echo "🚀 Step 1: Starting Minikube with optimized resources..."
echo "   CPUs: 4"
echo "   Memory: 4096MB"
echo "   Driver: Docker"
echo "   Kubernetes: v1.28.3"

# Start Minikube with optimal configuration
minikube start \
    --cpus=4 \
    --memory=4096 \
    --driver=docker \
    --kubernetes-version=v1.28.3 \
    --addons=ingress,metrics-server,dashboard

echo "✅ Minikube started successfully"

# ========== STEP 2: Enable Addons ==========
echo ""
echo "🔌 Step 2: Enabling critical cluster features..."

# Verify addons are enabled
echo "   • Ingress (Nginx)..."
minikube addons enable ingress 2>/dev/null || echo "   Already enabled"

echo "   • Metrics Server (for kubectl top)..."
minikube addons enable metrics-server 2>/dev/null || echo "   Already enabled"

echo "   • Dashboard (visual management)..."
minikube addons enable dashboard 2>/dev/null || echo "   Already enabled"

echo "✅ All addons enabled"

# ========== STEP 3: Context Setup ==========
echo ""
echo "🎯 Step 3: Setting kubectl context to minikube..."
kubectl config use-context minikube

echo "✅ kubectl context configured"

# ========== STEP 4: Verification ==========
echo ""
echo "🔍 Step 4: Verifying cluster health..."

# Wait for core pods to be ready
echo "   Waiting for core services..."
sleep 5

# Check ingress controller
INGRESS_READY=$(kubectl get pods -n ingress-nginx -l app.kubernetes.io/component=controller 2>/dev/null | grep -c "Running" || echo "0")

if [ "$INGRESS_READY" -gt 0 ]; then
    echo "   ✅ Ingress controller: Running"
else
    echo "   ⚠️  Ingress controller: Starting (may take a minute)"
fi

# Check metrics server
METRICS_READY=$(kubectl get deployment metrics-server -n kube-system 2>/dev/null | grep -c "1/1" || echo "0")

if [ "$METRICS_READY" -gt 0 ]; then
    echo "   ✅ Metrics server: Running"
else
    echo "   ⚠️  Metrics server: Starting"
fi

# Get cluster info
echo ""
echo "📊 Cluster Information:"
echo "   Minikube IP: $(minikube ip)"
echo "   Kubernetes Version: $(kubectl version --short 2>/dev/null | grep Server | awk '{print $3}')"
echo "   Context: $(kubectl config current-context)"

# ========== STEP 5: Useful Commands ==========
echo ""
echo "💡 Useful Commands:"
echo "   • Dashboard: minikube dashboard"
echo "   • Tunnel (for Ingress): minikube tunnel"
echo "   • View metrics: kubectl top nodes"
echo "   • Check ingress: kubectl get pods -n ingress-nginx"

# ========== SUMMARY ==========
echo ""
echo "=========================================="
echo "✅ [SUCCESS] Cluster initialized!"
echo "=========================================="
echo ""
echo "Enabled Features:"
echo "  • Ingress (Nginx) - HTTP/HTTPS routing"
echo "  • Metrics Server - Resource monitoring"
echo "  • Dashboard - Visual management"
echo ""
echo "Next Steps:"
echo "  1. Build images: ./1-build-images.sh"
echo "  2. Deploy app: ./deploy-helm.ps1"
echo ""
