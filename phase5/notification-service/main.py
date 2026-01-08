"""
Notification Service for Todo Application - Phase 5

This service subscribes to task events from Kafka via Dapr and processes them.
It demonstrates the event-driven architecture pattern with Dapr pub/sub.

Author: Tahir Yamin <tahiryamin2050@gmail.com>
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime

app = FastAPI(
    title="Todo Notification Service",
    description="Processes task events and sends notifications",
    version="1.0.0"
)

# Dapr configuration
DAPR_PUBSUB_NAME = "kafka-pubsub"

class CloudEvent(BaseModel):
    """Cloud Events v1.0 format for Dapr pub/sub"""
    id: str
    source: str
    specversion: str
    type: str
    datacontenttype: str = "application/json"
    data: Dict[str, Any]

@app.get("/dapr/subscribe")
async def subscribe():
    """Dapr subscription configuration"""
    return [
        {
            "pubsubname": DAPR_PUBSUB_NAME,
            "topic": "task-events",
            "route": "/handle-task-event"
        },
        {
            "pubsubname": DAPR_PUBSUB_NAME,
            "topic": "activity-log-events",
            "route": "/handle-activity-event"
        }
    ]

@app.post("/handle-task-event")
async def handle_task_event(event: CloudEvent):
    """Handle task events"""
    data = event.data
    action = data.get("action", "unknown")
    task_id = data.get("task_id")
    task_data = data.get("data", {})
    
    print(f"\n{'='*60}")
    print(f"🔔 TASK EVENT RECEIVED")
    print(f"   Action: {action.upper()}")
    print(f"   Task ID: {task_id}")
    print(f"   Title: {task_data.get('title', 'Unknown')}")
    print(f"   Timestamp: {datetime.now().isoformat()}")
    print(f"{'='*60}\n")
    
    return {"success": True}

@app.post("/handle-activity-event")
async def handle_activity_event(event: CloudEvent):
    """Handle activity events"""
    print(f"📊 Activity event: {event.data}")
    return {"success": True}

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "notification"}

if __name__ == "__main__":
    import uvicorn
    import os
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8001)))
