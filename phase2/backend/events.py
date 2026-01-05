"""
Phase 5: Event-Driven Architecture Module

This module provides event publishing functionality using Dapr Pub/Sub.
Events are published to Kafka topics via Dapr sidecar for:
- Task CRUD operations
- Reminders
- Real-time client sync

Source: Phase 5 Implementation Plan
Credits: Dapr Python SDK patterns from dapr/quickstarts
"""

import os
import httpx
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum

# Dapr sidecar URL (default localhost:3500)
DAPR_HOST = os.getenv("DAPR_HOST", "localhost")
DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", "3500")
DAPR_URL = f"http://{DAPR_HOST}:{DAPR_HTTP_PORT}"

# Pub/Sub configuration
PUBSUB_NAME = os.getenv("DAPR_PUBSUB_NAME", "kafka-pubsub")


class EventType(str, Enum):
    """Task event types for Kafka topics."""
    CREATED = "created"
    UPDATED = "updated"
    COMPLETED = "completed"
    DELETED = "deleted"
    REMINDER_SET = "reminder_set"
    REMINDER_DUE = "reminder_due"
    RECURRENCE_TRIGGERED = "recurrence_triggered"


class KafkaTopic(str, Enum):
    """Kafka topics for event routing."""
    TASK_EVENTS = "task-events"
    REMINDERS = "reminders"
    TASK_UPDATES = "task-updates"


async def publish_event(
    topic: KafkaTopic,
    event_type: EventType,
    data: Dict[str, Any],
    user_id: Optional[str] = None
) -> bool:
    """
    Publish an event to Kafka via Dapr Pub/Sub.
    
    Args:
        topic: Target Kafka topic
        event_type: Type of event (created, updated, etc.)
        data: Event payload
        user_id: User who triggered the event
    
    Returns:
        True if published successfully, False otherwise
    
    Example:
        await publish_event(
            KafkaTopic.TASK_EVENTS,
            EventType.CREATED,
            {"task_id": 123, "title": "New task"},
            user_id="user-123"
        )
    """
    event_payload = {
        "event_type": event_type.value,
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": user_id,
        "data": data
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{DAPR_URL}/v1.0/publish/{PUBSUB_NAME}/{topic.value}",
                json=event_payload,
                headers={"Content-Type": "application/json"},
                timeout=5.0
            )
            response.raise_for_status()
            return True
    except httpx.HTTPStatusError as e:
        print(f"[Events] Failed to publish to {topic.value}: {e.response.status_code}")
        return False
    except Exception as e:
        print(f"[Events] Error publishing event: {e}")
        return False


async def publish_task_event(
    event_type: EventType,
    task_data: Dict[str, Any],
    user_id: str
) -> bool:
    """
    Publish a task event to the task-events topic.
    
    Args:
        event_type: CREATED, UPDATED, COMPLETED, or DELETED
        task_data: Full task object
        user_id: User who performed the action
    
    Returns:
        True if published successfully
    """
    return await publish_event(
        topic=KafkaTopic.TASK_EVENTS,
        event_type=event_type,
        data={
            "task_id": task_data.get("id"),
            "task": task_data
        },
        user_id=user_id
    )


async def schedule_reminder(
    task_id: str,
    task_title: str,
    remind_at: datetime,
    due_at: Optional[datetime],
    user_id: str
) -> bool:
    """
    Publish a reminder event to be processed at the scheduled time.
    
    This uses Dapr Jobs API for exact-time scheduling instead of cron polling.
    
    Args:
        task_id: ID of the task
        task_title: Title for notification display
        remind_at: When to trigger the reminder
        due_at: When the task is due
        user_id: User to notify
    
    Returns:
        True if scheduled successfully
    """
    return await publish_event(
        topic=KafkaTopic.REMINDERS,
        event_type=EventType.REMINDER_SET,
        data={
            "task_id": task_id,
            "title": task_title,
            "remind_at": remind_at.isoformat(),
            "due_at": due_at.isoformat() if due_at else None
        },
        user_id=user_id
    )


async def publish_task_update_for_sync(
    task_id: str,
    action: str,
    task_data: Optional[Dict[str, Any]] = None
) -> bool:
    """
    Publish task update for real-time client synchronization.
    
    Clients connected via WebSocket can subscribe to this topic
    to receive live updates when tasks change.
    
    Args:
        task_id: ID of the updated task
        action: What changed (created, updated, deleted)
        task_data: Optional full task data
    
    Returns:
        True if published successfully
    """
    return await publish_event(
        topic=KafkaTopic.TASK_UPDATES,
        event_type=EventType.UPDATED,
        data={
            "task_id": task_id,
            "action": action,
            "task": task_data
        }
    )


# --- Dapr Jobs API for Exact-Time Reminders ---

async def schedule_reminder_job(
    task_id: str,
    remind_at: datetime,
    user_id: str
) -> bool:
    """
    Schedule a reminder using Dapr Jobs API for exact-time delivery.
    
    Unlike cron polling, this triggers at the exact scheduled time.
    Dapr will call back to /api/jobs/trigger when the time comes.
    
    Args:
        task_id: Task to remind about
        remind_at: Exact time to trigger
        user_id: User to notify
    
    Returns:
        True if job scheduled successfully
    
    Reference: Dapr Jobs API (alpha)
    Docs: https://docs.dapr.io/reference/api/jobs_api/
    """
    job_name = f"reminder-task-{task_id}"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{DAPR_URL}/v1.0-alpha1/jobs/{job_name}",
                json={
                    "dueTime": remind_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "data": {
                        "task_id": task_id,
                        "user_id": user_id,
                        "type": "reminder"
                    }
                },
                timeout=5.0
            )
            response.raise_for_status()
            print(f"[Events] Scheduled reminder job {job_name} for {remind_at}")
            return True
    except Exception as e:
        print(f"[Events] Failed to schedule reminder job: {e}")
        return False


async def cancel_reminder_job(task_id: str) -> bool:
    """
    Cancel a previously scheduled reminder job.
    
    Args:
        task_id: Task whose reminder to cancel
    
    Returns:
        True if cancelled successfully
    """
    job_name = f"reminder-task-{task_id}"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{DAPR_URL}/v1.0-alpha1/jobs/{job_name}",
                timeout=5.0
            )
            # 404 is OK - job might not exist
            if response.status_code == 404:
                return True
            response.raise_for_status()
            return True
    except Exception as e:
        print(f"[Events] Failed to cancel reminder job: {e}")
        return False
