"""
Dapr Integration Module for Todo Backend

This module handles:
1. Dapr pub/sub subscriptions (subscribing to Kafka topics)
2. Event publishing (publishing to Kafka via Dapr)  
3. State management (using Dapr state API with Redis)

Author: Tahir Yamin <tahiryamin2050@gmail.com>
"""

import httpx
import json
from typing import Dict, Any, List
from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="", tags=["dapr"])

# Dapr configuration
DAPR_HTTP_PORT = "3500"
DAPR_PUBSUB_NAME = "kafka-pubsub"
DAPR_STATE_STORE = "statestore"

# ========== PUB/SUB SUBSCRIPTIONS ==========

class CloudEvent(BaseModel):
    """Cloud Events v1.0 format for Dapr pub/sub"""
    id: str
    source: str
    specversion: str
    type: str
    datacontenttype: str = "application/json"
    data: Dict[str, Any]

@router.get("/dapr/subscribe")
async def subscribe():
    """
    Dapr calls this endpoint to get subscription configuration.
    Returns list of topics to subscribe to and their routes.
    """
    subscriptions = [
        {
            "pubsubname": DAPR_PUBSUB_NAME,
            "topic": "task-events",
            "route": "/events/task"
        },
        {
            "pubsubname": DAPR_PUBSUB_NAME,
            "topic": "activity-log-events",
            "route": "/events/activity"
        }
    ]
    
    print(f"🔔 Dapr subscribed to {len(subscriptions)} topics")
    return subscriptions

@router.post("/events/task")
async def handle_task_event(event: CloudEvent):
    """Handle task events from Kafka via Dapr"""
    try:
        data = event.data
        action = data.get("action", "unknown")
        task_id = data.get("task_id")
        
        print(f"📥 Task Event Received: {action} - Task ID: {task_id}")
        print(f"   Data: {json.dumps(data, indent=2)}")
        
        # Process based on action type
        if action == "created":
            print(f"✅ Task {task_id} created")
        elif action == "completed":
            print(f"✅ Task {task_id} marked complete")
        elif action == "updated":
            print(f"✅ Task {task_id} updated")
        elif action == "deleted":
            print(f"✅ Task {task_id} deleted")
        
        return {"success": True, "processed": action}
    
    except Exception as e:
        print(f"❌ Error processing task event: {e}")
        return {"success": False, "error": str(e)}

@router.post("/events/activity")
async def handle_activity_event(event: CloudEvent):
    """Handle activity log events from Kafka via Dapr"""
    try:
        data = event.data
        user_email = data.get("user_email", "unknown")
        change_type = data.get("change_type", "unknown")
        
        print(f"📥 Activity Event: {change_type} by {user_email}")
        print(f"   Data: {json.dumps(data, indent=2)}")
        
        return {"success": True}
    
    except Exception as e:
        print(f"❌ Error processing activity event: {e}")
        return {"success": False, "error": str(e)}

# ========== EVENT PUBLISHING ==========

async def publish_event(topic: str, data: Dict[str, Any]):
    """
    Publish an event to Kafka via Dapr pub/sub.
    
    Args:
        topic: Kafka topic name (task-events, activity-log-events)
        data: Event payload (must be JSON serializable)
    """
    try:
        url = f"http://localhost:{DAPR_HTTP_PORT}/v1.0/publish/{DAPR_PUBSUB_NAME}/{topic}"
        
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(url, json=data)
            
            if response.status_code == 200 or response.status_code == 204:
                print(f"📤 Published to {topic}: {data.get('action', 'event')}")
                return True
            else:
                print(f"⚠️ Publish failed ({response.status_code}): {response.text}")
                return False
                
    except httpx.TimeoutException:
        print(f"⏱️ Timeout publishing to {topic}")
        return False
    except Exception as e:
        print(f"❌ Error publishing event: {e}")
        return False

async def publish_task_event(action: str, task_id: int, task_data: Dict[str, Any]):
    """Convenience function to publish task events"""
    event = {
        "action": action,
        "task_id": task_id,
        "data": task_data,
        "timestamp": str(task_data.get("updated_at") or task_data.get("created_at"))
    }
    await publish_event("task-events", event)

async def publish_activity_event(user_email: str, change_type: str, details: Dict[str, Any]):
    """Convenience function to publish activity log events"""
    event = {
        "user_email": user_email,
        "change_type": change_type,
        "details": details,
        "timestamp": details.get("created_at")
    }
    await publish_event("activity-log-events", event)

# ========== STATE MANAGEMENT ==========

async def save_state(key: str, value: Any):
    """Save state to Redis via Dapr state API"""
    try:
        url = f"http://localhost:{DAPR_HTTP_PORT}/v1.0/state/{DAPR_STATE_STORE}"
        
        payload = [{
            "key": key,
            "value": value
        }]
        
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(url, json=payload)
            
            if response.status_code in [200, 201, 204]:
                print(f"💾 Saved state: {key}")
                return True
            else:
                print(f"⚠️ State save failed: {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Error saving state: {e}")
        return False

async def get_state(key: str) -> Any:
    """Get state from Redis via Dapr state API"""
    try:
        url = f"http://localhost:{DAPR_HTTP_PORT}/v1.0/state/{DAPR_STATE_STORE}/{key}"
        
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url)
            
            if response.status_code == 200:
                data = response.json()
                print(f"📖 Retrieved state: {key}")
                return data
            elif response.status_code == 204:
                print(f"📭 No state found for: {key}")
                return None
            else:
                print(f"⚠️ State get failed: {response.text}")
                return None
                
    except Exception as e:
        print(f"❌ Error getting state: {e}")
        return None

async def delete_state(key: str):
    """Delete state from Redis via Dapr state API"""
    try:
        url = f"http://localhost:{DAPR_HTTP_PORT}/v1.0/state/{DAPR_STATE_STORE}/{key}"
        
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.delete(url)
            
            if response.status_code in [200, 204]:
                print(f"🗑️ Deleted state: {key}")
                return True
            else:
                print(f"⚠️ State delete failed: {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Error deleting state: {e}")
        return False

# ========== STATE MANAGEMENT API ENDPOINTS ==========

@router.post("/api/state/{key}")
async def save_user_state(key: str, value: Dict[str, Any] = Body(...)):
    """API endpoint to save user state (preferences, caches, etc.)"""
    success = await save_state(key, value)
    if success:
        return {"success": True, "key": key}
    else:
        raise HTTPException(status_code=500, detail="Failed to save state")

@router.get("/api/state/{key}")
async def get_user_state(key: str):
    """API endpoint to retrieve user state"""
    value = await get_state(key)
    if value is not None:
        return {"success": True, "key": key, "value": value}
    else:
        return {"success": True, "key": key, "value": None}

@router.delete("/api/state/{key}")
async def delete_user_state(key: str):
    """API endpoint to delete user state"""
    success = await delete_state(key)
    if success:
        return {"success": True, "key": key}
    else:
        raise HTTPException(status_code=500, detail="Failed to delete state")
