"""
Notification Service - Phase 5 Kafka Consumer

This service subscribes to Kafka topics via Dapr Pub/Sub and handles:
- Reminder notifications
- Task update notifications (for WebSocket broadcast)
- Event logging

Source: Phase 5 Implementation Plan
Credits: Patterns from dapr/quickstarts and anthropics/claude-cookbooks
"""

import os
import uvicorn
from datetime import datetime
from typing import Optional, Dict, Any
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel

# Service configuration
SERVICE_NAME = "notification-service"
SERVICE_PORT = int(os.getenv("PORT", "8001"))
DAPR_PUBSUB_NAME = os.getenv("DAPR_PUBSUB_NAME", "kafka-pubsub")

app = FastAPI(
    title="Todo Notification Service",
    description="Kafka consumer for task reminders and notifications",
    version="1.0.0"
)


# --- Models ---

class CloudEvent(BaseModel):
    """CloudEvents format used by Dapr Pub/Sub."""
    id: str
    source: str
    type: str
    specversion: str = "1.0"
    datacontenttype: str = "application/json"
    data: Dict[str, Any]


class ReminderEvent(BaseModel):
    """Reminder event payload."""
    event_type: str
    timestamp: str
    user_id: Optional[str]
    data: Dict[str, Any]


# --- Health Endpoints ---

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": SERVICE_NAME}

@app.get("/healthz")
async def healthz():
    """Kubernetes liveness probe."""
    return {"status": "ok"}


# --- Dapr Pub/Sub Subscription Declaration ---

@app.get("/dapr/subscribe")
async def subscribe():
    """
    Dapr subscription declaration.
    
    This endpoint tells Dapr which topics to subscribe to and
    which routes handle each subscription.
    """
    return [
        {
            "pubsubname": DAPR_PUBSUB_NAME,
            "topic": "reminders",
            "route": "/events/reminders"
        },
        {
            "pubsubname": DAPR_PUBSUB_NAME,
            "topic": "task-events",
            "route": "/events/tasks"
        },
        {
            "pubsubname": DAPR_PUBSUB_NAME,
            "topic": "task-updates",
            "route": "/events/updates"
        }
    ]


# --- Event Handlers ---

@app.post("/events/reminders")
async def handle_reminder(request: Request):
    """
    Handle reminder events from Kafka.
    
    When a reminder is due, this endpoint receives the event
    and triggers the appropriate notification.
    """
    try:
        body = await request.json()
        print(f"📩 Received reminder event: {body}")
        
        event_data = body.get("data", {})
        event_type = event_data.get("event_type")
        user_id = event_data.get("user_id")
        data = event_data.get("data", {})
        
        if event_type == "reminder_set":
            print(f"⏰ Reminder scheduled: {data.get('title')} at {data.get('remind_at')}")
            # In production: Schedule actual notification delivery
            
        elif event_type == "reminder_due":
            print(f"🔔 REMINDER DUE: {data.get('title')} for user {user_id}")
            # In production: Send push notification, email, or WebSocket message
            await send_notification(user_id, data)
        
        return {"success": True, "status": "processed"}
        
    except Exception as e:
        print(f"❌ Error handling reminder: {e}")
        return {"success": False, "error": str(e)}


@app.post("/events/tasks")
async def handle_task_event(request: Request):
    """
    Handle task CRUD events from Kafka.
    
    These events can be used for:
    - Activity logging
    - Analytics
    - Webhooks to external systems
    """
    try:
        body = await request.json()
        print(f"📩 Received task event: {body}")
        
        event_data = body.get("data", {})
        event_type = event_data.get("event_type")
        user_id = event_data.get("user_id")
        data = event_data.get("data", {})
        
        # Log event for analytics
        log_event(event_type, user_id, data)
        
        # Handle specific event types
        if event_type == "created":
            print(f"➕ Task created: {data.get('task', {}).get('title')}")
        elif event_type == "updated":
            print(f"✏️ Task updated: {data.get('task', {}).get('title')}")
        elif event_type == "completed":
            print(f"✅ Task completed: {data.get('task', {}).get('title')}")
        elif event_type == "deleted":
            print(f"🗑️ Task deleted: {data.get('title')}")
        
        return {"success": True, "status": "processed"}
        
    except Exception as e:
        print(f"❌ Error handling task event: {e}")
        return {"success": False, "error": str(e)}


@app.post("/events/updates")
async def handle_real_time_update(request: Request):
    """
    Handle real-time task updates for client sync.
    
    These events are broadcast to connected WebSocket clients
    for live updates without polling.
    """
    try:
        body = await request.json()
        print(f"📩 Received real-time update: {body}")
        
        event_data = body.get("data", {})
        action = event_data.get("data", {}).get("action")
        task_id = event_data.get("data", {}).get("task_id")
        
        # In production: Broadcast to WebSocket connections
        print(f"📡 Broadcasting update: {action} for task {task_id}")
        
        return {"success": True, "status": "broadcast_queued"}
        
    except Exception as e:
        print(f"❌ Error handling update: {e}")
        return {"success": False, "error": str(e)}


# --- Dapr Jobs Trigger Endpoint ---

@app.post("/api/jobs/trigger")
async def handle_job_trigger(request: Request):
    """
    Handle Dapr Jobs API callbacks.
    
    When a scheduled reminder job fires, Dapr calls this endpoint
    with the job data. We then process the reminder.
    """
    try:
        body = await request.json()
        print(f"⏰ Job triggered: {body}")
        
        job_data = body.get("data", {})
        job_type = job_data.get("type")
        
        if job_type == "reminder":
            task_id = job_data.get("task_id")
            user_id = job_data.get("user_id")
            
            # Fetch task details from backend or state store
            # For now, just log
            print(f"🔔 REMINDER TRIGGERED for task {task_id}, user {user_id}")
            
            await send_notification(user_id, {
                "task_id": task_id,
                "message": "Task reminder!"
            })
        
        return {"success": True, "status": "job_processed"}
        
    except Exception as e:
        print(f"❌ Error handling job trigger: {e}")
        return {"success": False, "error": str(e)}


# --- Helper Functions ---

async def send_notification(user_id: str, data: Dict[str, Any]):
    """
    Send notification to user.
    
    In production, this would:
    - Send push notification via Firebase/APNs
    - Send email via SendGrid/Resend
    - Broadcast via WebSocket
    - Send SMS via Twilio
    """
    print(f"📨 Sending notification to {user_id}: {data}")
    
    # TODO: Implement actual notification channels
    # For now, just log
    notification = {
        "user_id": user_id,
        "title": data.get("title", "Task Reminder"),
        "message": data.get("message", "You have a task due!"),
        "sent_at": datetime.utcnow().isoformat()
    }
    print(f"📤 Notification payload: {notification}")


def log_event(event_type: str, user_id: str, data: Dict[str, Any]):
    """Log event for analytics and debugging."""
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "user_id": user_id,
        "data": data
    }
    print(f"📝 Event log: {log_entry}")
    
    # TODO: Write to analytics database, send to logging service


# --- Application Startup ---

@app.on_event("startup")
async def startup():
    """Service startup handler."""
    print(f"🚀 {SERVICE_NAME} starting on port {SERVICE_PORT}")
    print(f"📡 Subscribing to pub/sub: {DAPR_PUBSUB_NAME}")
    print(f"📬 Topics: reminders, task-events, task-updates")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=SERVICE_PORT,
        reload=True
    )
