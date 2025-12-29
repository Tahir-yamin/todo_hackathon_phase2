"""
Docker Skills - Advanced Docker Management for AI Agents

This module provides Docker-specific capabilities for the Evolution Agent,
enabling autonomous build optimization, debugging, and repair.

Following the AgentSkills and MCP (Model Context Protocol) standards.
"""

import subprocess
import json
import re
from typing import Dict, Any, List, Optional
from datetime import datetime
import os


class DockerSkillSet:
    """
    Advanced AI Skills for Docker Management.
    
    These skills enable the agent to:
    - Monitor container resource usage
    - Verify build artifacts (like Prisma binaries)
    - Analyze and optimize image layers
    - Detect and fix build failures
    - Suggest security improvements
    """
    
    def __init__(self):
        self.common_issues = {
            "ETIMEDOUT": {
                "pattern": r"ETIMEDOUT|timeout|fetch.*failed",
                "fix": "Add npm retry configuration or use retry loops"
            },
            "PrismaClientInitializationError": {
                "pattern": r"PrismaClientInitializationError|prisma.*engine|Query engine.*not found",
                "fix": "Add binaryTargets to schema.prisma for target OS"
            },
            "GoogleFonts": {
                "pattern": r"Failed to fetch.*Google Fonts|next/font.*error",
                "fix": "Comment out Google Fonts import or use NEXT_FONT_GOOGLE_MOCKED_RESPONSES"
            },
            "ENOSPC": {
                "pattern": r"ENOSPC|no space left",
                "fix": "Clean Docker system: docker system prune -a"
            }
        }

    def analyze_container_stats(self, container_name: str) -> Dict[str, Any]:
        """
        Get real-time resource statistics for a container.
        
        Returns CPU%, Memory%, Network I/O, and Block I/O.
        """
        try:
            cmd = f"docker stats {container_name} --no-stream --format json"
            result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
            stats = json.loads(result.decode('utf-8'))
            
            # Parse and clean up the stats
            return {
                "status": "success",
                "container": container_name,
                "cpu_percent": stats.get("CPUPerc", "N/A"),
                "memory_usage": stats.get("MemUsage", "N/A"),
                "memory_percent": stats.get("MemPerc", "N/A"),
                "network_io": stats.get("NetIO", "N/A"),
                "block_io": stats.get("BlockIO", "N/A"),
                "pids": stats.get("PIDs", "N/A"),
                "timestamp": datetime.utcnow().isoformat()
            }
        except subprocess.CalledProcessError as e:
            return {
                "status": "error",
                "message": f"Failed to get stats: {e.output.decode('utf-8')}"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def verify_prisma_binary(self, container_name: str) -> Dict[str, Any]:
        """
        Verify that the correct Prisma engine binary exists in the container.
        
        This checks for the linux-musl-openssl-3.0.x binary required by Alpine.
        """
        try:
            # Check if .prisma directory exists
            check_cmd = f"docker exec {container_name} ls /app/node_modules/.prisma/client"
            result = subprocess.check_output(check_cmd, shell=True, stderr=subprocess.STDOUT)
            files = result.decode('utf-8').strip().split('\n')
            
            # Look for the correct binary
            has_linux_musl = any('linux-musl' in f or 'libquery_engine' in f for f in files)
            
            if has_linux_musl:
                return {
                    "status": "verified",
                    "message": "Correct Prisma binary found",
                    "files": files,
                    "binary_target": "linux-musl-openssl-3.0.x"
                }
            else:
                return {
                    "status": "missing",
                    "message": "linux-musl binary not found",
                    "files": files,
                    "fix_action": "Add binaryTargets = ['native', 'linux-musl-openssl-3.0.x'] to schema.prisma"
                }
        except subprocess.CalledProcessError as e:
            return {
                "status": "error",
                "message": "Could not access Prisma directory",
                "fix_action": "Ensure Prisma client is generated during build"
            }

    def analyze_image_layers(self, image_name: str) -> Dict[str, Any]:
        """
        Analyze Docker image layers to identify optimization opportunities.
        
        Uses `docker history` to show layer sizes.
        """
        try:
            cmd = f"docker history {image_name} --no-trunc --format json"
            result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
            
            # Parse each line as JSON
            layers = []
            for line in result.decode('utf-8').strip().split('\n'):
                if line:
                    layer = json.loads(line)
                    layers.append({
                        "created": layer.get("CreatedAt", ""),
                        "size": layer.get("Size", ""),
                        "comment": layer.get("Comment", ""),
                        "created_by": layer.get("CreatedBy", "")[:100]  # Truncate for readability
                    })
            
            # Calculate total size
            total_size_cmd = f"docker images {image_name} --format '{{{{.Size}}}}'"
            total_size = subprocess.check_output(total_size_cmd, shell=True).decode('utf-8').strip()
            
            # Identify large layers (potential optimization targets)
            large_layers = [l for l in layers if 'MB' in l['size'] or 'GB' in l['size']]
            
            return {
                "status": "success",
                "image": image_name,
                "total_size": total_size,
                "layer_count": len(layers),
                "large_layers": len(large_layers),
                "layers": layers[:10],  # Return top 10 for brevity
                "optimization_tips": [
                    "Combine RUN commands to reduce layers",
                    "Use multi-stage builds to exclude build tools",
                    "Order COPY commands by change frequency"
                ]
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def detect_build_failures(self, build_log: str) -> Dict[str, Any]:
        """
        Analyze Docker build log to detect common failure patterns.
        
        Returns detected issues and suggested fixes.
        """
        detected_issues = []
        suggested_fixes = []
        
        for issue_name, issue_info in self.common_issues.items():
            if re.search(issue_info['pattern'], build_log, re.IGNORECASE):
                detected_issues.append(issue_name)
                suggested_fixes.append({
                    "issue": issue_name,
                    "fix": issue_info['fix']
                })
        
        # Additional analysis
        if "Exit code: 1" in build_log and not detected_issues:
            detected_issues.append("Generic build failure")
            suggested_fixes.append({
                "issue": "Generic build failure",
                "fix": "Check the error log for specific error messages"
            })
        
        return {
            "status": "analyzed",
            "issues_found": len(detected_issues),
            "issues": detected_issues,
            "fixes": suggested_fixes,
            "log_excerpt": build_log[-500:] if len(build_log) > 500 else build_log
        }

    def suggest_dockerfile_fixes(self, dockerfile_path: str, detected_issues: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Analyze Dockerfile and suggest improvements.
        """
        suggestions = []
        
        try:
            with open(dockerfile_path, 'r') as f:
                dockerfile_content = f.read()
            
            # Check for common issues
            if 'npm install' in dockerfile_content and 'fetch-retries' not in dockerfile_content:
                suggestions.append({
                    "issue": "No retry configuration for npm",
                    "fix": "Add: RUN npm config set fetch-retries 5 && npm config set fetch-retry-mintimeout 20000"
                })
            
            if 'prisma' in dockerfile_content.lower() and 'npx prisma generate' not in dockerfile_content:
                suggestions.append({
                    "issue": "Prisma not explicitly generated",
                    "fix": "Add: RUN npx prisma generate"
                })
            
            if 'FROM node' in dockerfile_content and 'AS' not in dockerfile_content:
                suggestions.append({
                    "issue": "Not using multi-stage build",
                    "fix": "Use multi-stage: FROM node:20-alpine AS deps, AS builder, AS runner"
                })
            
            if '.dockerignore' not in os.listdir(os.path.dirname(dockerfile_path)):
                suggestions.append({
                    "issue": "Missing .dockerignore file",
                    "fix": "Create .dockerignore to exclude node_modules, .git, .next, etc."
                })
            
            return {
                "status": "analyzed",
                "dockerfile": dockerfile_path,
                "suggestions": suggestions,
                "best_practices_score": f"{max(0, 100 - len(suggestions) * 20)}%"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def compare_image_sizes(self, image_before: str, image_after: str) -> Dict[str, Any]:
        """
        Compare sizes of two images to measure optimization impact.
        """
        try:
            def get_size_bytes(image_name):
                cmd = f"docker inspect {image_name} --format '{{{{.Size}}}}'"
                result = subprocess.check_output(cmd, shell=True)
                return int(result.decode('utf-8').strip())
            
            size_before = get_size_bytes(image_before)
            size_after = get_size_bytes(image_after)
            
            reduction = size_before - size_after
            reduction_percent = (reduction / size_before * 100) if size_before > 0 else 0
            
            return {
                "status": "compared",
                "image_before": {
                    "name": image_before,
                    "size_bytes": size_before,
                    "size_mb": round(size_before / 1024 / 1024, 2)
                },
                "image_after": {
                    "name": image_after,
                    "size_bytes": size_after,
                    "size_mb": round(size_after / 1024 / 1024, 2)
                },
                "reduction": {
                    "bytes": reduction,
                    "mb": round(reduction / 1024 / 1024, 2),
                    "percent": round(reduction_percent, 2)
                },
                "optimization_result": "Success" if reduction > 0 else "No improvement"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def check_security_vulnerabilities(self, image_name: str) -> Dict[str, Any]:
        """
        Basic security check for Docker image.
        
        Note: For production, integrate with Trivy or Snyk.
        """
        checks = {
            "running_as_root": False,
            "latest_tag_used": False,
            "secrets_in_env": False
        }
        
        try:
            # Check if running as root
            cmd = f"docker inspect {image_name} --format '{{{{.Config.User}}}}'"
            user = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
            checks["running_as_root"] = (user == "" or user == "root")
            
            # Check if using latest tag
            checks["latest_tag_used"] = ":latest" in image_name or ":" not in image_name
            
            # Check for exposed secrets in env
            env_cmd = f"docker inspect {image_name} --format '{{{{json .Config.Env}}}}'"
            env_vars = subprocess.check_output(env_cmd, shell=True).decode('utf-8')
            checks["secrets_in_env"] = any(word in env_vars.lower() for word in ['password', 'secret', 'key', 'token'])
            
            issues = []
            if checks["running_as_root"]:
                issues.append("Container runs as root (security risk)")
            if checks["latest_tag_used"]:
                issues.append("Using 'latest' tag (unpredictable)")
            if checks["secrets_in_env"]:
                issues.append("Possible secrets in environment variables")
            
            return {
                "status": "scanned",
                "image": image_name,
                "checks": checks,
                "issues": issues,
                "security_score": f"{max(0, 100 - len(issues) * 30)}%",
                "recommendation": "Use Trivy or Snyk for comprehensive vulnerability scanning"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def optimize_build_cache(self, dockerfile_path: str) -> Dict[str, Any]:
        """
        Analyze Dockerfile for cache optimization opportunities.
        """
        suggestions = []
        
        try:
            with open(dockerfile_path, 'r') as f:
                lines = f.readlines()
            
            # Check layer ordering
            copy_before_install = False
            for i, line in enumerate(lines):
                if 'COPY' in line and i < len(lines) - 1:
                    if 'RUN' in lines[i + 1] and ('install' in lines[i + 1] or 'npm' in lines[i + 1]):
                        copy_before_install = True
            
            if not copy_before_install:
                suggestions.append({
                    "optimization": "Improve cache hits",
                    "tip": "Copy package.json first, run install, then copy source code"
                })
            
            # Check for combined RUN commands
            run_count = sum(1 for line in lines if line.strip().startswith('RUN'))
            if run_count > 5:
                suggestions.append({
                    "optimization": "Reduce layers",
                    "tip": f"You have {run_count} RUN commands. Combine related commands with &&"
                })
            
            return {
                "status": "analyzed",
                "dockerfile": dockerfile_path,
                "cache_optimization_score": f"{max(0, 100 - len(suggestions) * 25)}%",
                "suggestions": suggestions
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }


#Singleton instance
docker_skills = DockerSkillSet()
