"""
Dapr Pub/Sub Integration for Phase 5
Zero-cost event streaming using Dapr sidecar (already deployed)
"""

import httpx
import os
from typing import Dict, Any
import asyncio

# Dapr configuration
DAPR_HOST = os.getenv("DAPR_HOST", "localhost")
DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", "3500")
DAPR_URL = f"http://{DAPR_HOST}:{DAPR_HTTP_PORT}"
DAPR_PUBSUB_NAME = "kafka-pubsub"  # Component name


async def publish_to_dapr(topic: str, data: Dict[str, Any]) -> bool:
    """
    Publish event to Dapr Pub/Sub (zero-cost, uses existing sidecar)
    
    Args:
        topic: Topic name (task-events, reminders, task-updates)
        data: Event data to publish
    
    Returns:
        True if published successfully
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{DAPR_URL}/v1.0/publish/{DAPR_PUBSUB_NAME}/{topic}",
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=5.0
            )
            response.raise_for_status()
            print(f"📤 Dapr: Published to {topic}")
            return True
    except httpx.HTTPStatusError as e:
        print(f"❌ Dapr publish failed: {e.response.status_code}")
        return False
    except Exception as e:
        print(f"⚠️ Dapr error: {e}")
        return False


def setup_dapr_integration(event_bus):
    """
    Integrate Dapr Pub/Sub with event bus (zero-cost)
    
    This bridges the in-memory event bus with Dapr,
    allowing future scaling to distributed systems
    
    Args:
        event_bus: SimpleEventBus instance
    """
    
    def publish_to_dapr_topic(event: dict):
        """Publish event to Dapr asynchronously"""
        event_type = event.get("event_type", "unknown")
        
        # Determine Dapr topic based on event type
        if "REMINDER" in event_type:
            topic = "reminders"
        elif event_type in ["TASK_CREATED", "TASK_UPDATED", "TASK_COMPLETED", "TASK_DELETED"]:
            topic = "task-events"
        else:
            topic = "task-updates"
        
        # Publish to Dapr (non-blocking)
        asyncio.create_task(publish_to_dapr(topic, event))
    
    # Subscribe to all events
    for event_type in ["TASK_CREATED", "TASK_UPDATED", "TASK_COMPLETED", "TASK_DELETED"]:
        event_bus.subscribe(event_type, publish_to_dapr_topic)
    
    print("✅ Dapr Pub/Sub integrated with event bus")
    print(f"   Dapr URL: {DAPR_URL}")
    print(f"   Topics: task-events, reminders, task-updates")


# Dapr subscription endpoint (for consuming messages)
def setup_dapr_subscriptions(app):
    """
    Setup Dapr subscription endpoints
    
    Dapr will call these endpoints when messages arrive
    """
    
    @app.get("/dapr/subscribe")
    async def dapr_subscribe():
        """Tell Dapr which topics to subscribe to"""
        return [
            {
                "pubsubname": DAPR_PUBSUB_NAME,
                "topic": "task-events",
                "route": "/dapr/task-events"
            },
            {
                "pubsubname": DAPR_PUBSUB_NAME,
                "topic": "reminders",
                "route": "/dapr/reminders"
            }
        ]
    
    @app.post("/dapr/task-events")
    async def handle_task_events(event: dict):
        """Handle task events from Dapr"""
        print(f"📥 Dapr received task event: {event.get('type')}")
        # Process event (e.g., update cache, trigger actions)
        return {"status": "SUCCESS"}
    
    @app.post("/dapr/reminders")
    async def handle_reminders(event: dict):
        """Handle reminder events from Dapr"""
        print(f"🔔 Dapr received reminder: {event}")
        # Send notification to user
        return {"status": "SUCCESS"}
    
    print("✅ Dapr subscription endpoints registered")


# Benefits of Dapr integration:
"""
1. Zero Infrastructure Cost:
   - Dapr sidecar already deployed
   - No additional pods needed
   - Uses existing Kubernetes infrastructure

2. Future Scalability:
   - Easy to swap in real Kafka/Redis
   - Distributed tracing built-in
   - Service-to-service mTLS

3. Cloud-Native Patterns:
   - Pub/Sub abstraction
   - Retry policies
   - Dead letter queues
"""
