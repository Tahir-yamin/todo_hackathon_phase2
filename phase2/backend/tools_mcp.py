#!/usr/bin/env python3
"""
Evolution Tool Hub - FastMCP Server (2025 Standard)
Kubernetes cluster management tools using official FastMCP library
"""

import sys
import io
import asyncio
import subprocess
import json
from typing import Dict, Any

# ========================================
# CRITICAL FIX FOR WINDOWS
# ========================================
# Force stdout to be UTF-8 with Unix newlines to prevent stream corruption
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer,
        encoding='utf-8',
        newline='\n',
        line_buffering=True
    )

# Save original stdout for FastMCP protocol
sys.stdout_original = sys.stdout

# Redirect all print() calls to stderr to avoid corrupting MCP stream
class StderrLogger:
    def write(self, message):
        sys.stderr.write(message)
    def flush(self):
        sys.stderr.flush()

sys.stdout = StderrLogger()

# ========================================
# Now safe to import FastMCP
# ========================================
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("EvolutionToolHub")


# ========================================
# TOOL IMPLEMENTATIONS
# ========================================

@mcp.tool()
def k8s_cluster_status() -> Dict[str, Any]:
    """
    Get the current status of all pods in the todo-chatbot namespace.
    Returns pod names, status, readiness, and restart counts.
    """
    try:
        result = subprocess.check_output(
            "kubectl get pods -n todo-chatbot -o json",
            shell=True,
            text=True,
            stderr=subprocess.PIPE
        )
        
        pods_data = json.loads(result)
        pods = []
        
        for item in pods_data.get("items", []):
            pods.append({
                "name": item["metadata"]["name"],
                "status": item["status"]["phase"],
                "ready": _get_ready_count(item),
                "restarts": _get_restart_count(item),
                "age": item["metadata"]["creationTimestamp"]
            })
        
        return {
            "status": "success",
            "namespace": "todo-chatbot",
            "pod_count": len(pods),
            "pods": pods
        }
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": str(e)}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {str(e)}"}


@mcp.tool()
def scale_deployment(deployment_name: str, replicas: int) -> Dict[str, Any]:
    """
    Scale a Kubernetes deployment to a specific number of replicas.
    
    Args:
        deployment_name: Name of deployment ('frontend' or 'backend')
        replicas: Number of replicas (0-5 for safety)
    
    Returns:
        Status and confirmation message
    """
    if deployment_name not in ["frontend", "backend"]:
        return {"status": "error", "message": "deployment_name must be 'frontend' or 'backend'"}
    
    if replicas < 0 or replicas > 5:
        return {"status": "error", "message": "replicas must be between 0 and 5"}
    
    try:
        full_name = f"evolution-todo-{deployment_name}"
        subprocess.check_output(
            f"kubectl scale deployment/{full_name} --replicas={replicas} -n todo-chatbot",
            shell=True,
            text=True,
            stderr=subprocess.PIPE
        )
        
        return {
            "status": "success",
            "deployment": deployment_name,
            "replicas": replicas,
            "message": f"Scaled {deployment_name} to {replicas} replicas"
        }
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": str(e)}


@mcp.tool()
def analyze_pod_logs(pod_name: str, lines: int = 50) -> Dict[str, Any]:
    """
    Retrieve the last N lines of logs from a specific pod for debugging.
    
    Args:
        pod_name: Name of the pod to analyze
        lines: Number of log lines to retrieve (default: 50)
    
    Returns:
        Pod logs and status
    """
    try:
        result = subprocess.check_output(
            f"kubectl logs {pod_name} -n todo-chatbot --tail={lines}",
            shell=True,
            text=True,
            stderr=subprocess.PIPE
        )
        
        return {
            "status": "success",
            "pod": pod_name,
            "lines_retrieved": lines,
            "logs": result[:2000]  # Truncate for readability
        }
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": str(e)}


@mcp.tool()
def get_service_endpoints() -> Dict[str, Any]:
    """
    List all service endpoints and their URLs in the todo-chatbot namespace.
    Shows service names, types, cluster IPs, and ports.
    """
    try:
        result = subprocess.check_output(
            "kubectl get svc -n todo-chatbot -o json",
            shell=True,
            text=True,
            stderr=subprocess.PIPE
        )
        
        svc_data = json.loads(result)
        services = []
        
        for item in svc_data.get("items", []):
            services.append({
                "name": item["metadata"]["name"],
                "type": item["spec"]["type"],
                "cluster_ip": item["spec"].get("clusterIP"),
                "ports": item["spec"].get("ports", [])
            })
        
        return {
            "status": "success",
            "service_count": len(services),
            "services": services
        }
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": str(e)}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {str(e)}"}


@mcp.tool()
def health_check_full() -> Dict[str, Any]:
    """
    Perform a comprehensive health check across all services in the cluster.
    Checks pod status, service endpoints, and overall cluster health.
    """
    cluster_status = k8s_cluster_status()
    service_endpoints = get_service_endpoints()
    
    all_pods_healthy = all(
        pod.get("status") == "Running"
        for pod in cluster_status.get("pods", [])
    )
    
    return {
        "status": "healthy" if all_pods_healthy else "degraded",
        "cluster": cluster_status,
        "services": service_endpoints,
        "summary": {
            "total_pods": cluster_status.get("pod_count", 0),
            "healthy_pods": sum(1 for p in cluster_status.get("pods", []) if p.get("status") == "Running"),
            "total_services": service_endpoints.get("service_count", 0)
        }
    }


# ========================================
# HELPER FUNCTIONS
# ========================================

def _get_ready_count(pod_item: Dict) -> str:
    """Parse container readiness from pod status"""
    try:
        statuses = pod_item["status"]["containerStatuses"]
        ready = sum(1 for s in statuses if s["ready"])
        total = len(statuses)
        return f"{ready}/{total}"
    except (KeyError, TypeError):
        return "0/0"


def _get_restart_count(pod_item: Dict) -> int:
    """Count total restarts across all containers"""
    try:
        statuses = pod_item["status"]["containerStatuses"]
        return sum(s["restartCount"] for s in statuses)
    except (KeyError, TypeError):
        return 0


# ========================================
# SERVER STARTUP
# ========================================

if __name__ == "__main__":
    # Restore original stdout for FastMCP protocol communication
    sys.stdout = sys.stdout_original
    
    # Start the FastMCP server
    mcp.run()
