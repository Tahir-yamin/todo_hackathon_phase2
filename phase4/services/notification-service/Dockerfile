# Notification Service - Phase 5
# ==============================
#
# Multi-stage Docker build for the notification service.
# Uses Dapr sidecar pattern for Kafka pub/sub.
#
# Build:
#   docker build -t notification-service .
#
# Run with Dapr:
#   dapr run --app-id notification-service --app-port 8001 -- python main.py

FROM python:3.11-slim AS base

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY main.py .

# Expose port
EXPOSE 8001

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

# Run
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
