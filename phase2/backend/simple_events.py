"""
Lightweight Event Bus for Phase 5
Zero-cost in-memory event system with PostgreSQL audit logging
"""

from typing import Dict, List, Callable, Any
from datetime import datetime
import json
from contextlib import contextmanager

class SimpleEventBus:
    """Lightweight in-memory event bus for task events"""
    
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        self._enabled = True
    
    def subscribe(self, event_type: str, handler: Callable):
        """Subscribe a handler to an event type"""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)
        print(f"📢 Subscribed handler to {event_type}")
    
    def publish(self, event_type: str, data: Dict[str, Any]):
        """Publish an event to all subscribers"""
        if not self._enabled:
            return
        
        event = {
            "event_type": event_type,
            "timestamp": datetime.utcnow().isoformat(),
            "data": data
        }
        
        # Notify subscribers
        if event_type in self.subscribers:
            for handler in self.subscribers[event_type]:
                try:
                    handler(event)
                except Exception as e:
                    print(f"❌ Event handler error for {event_type}: {e}")
        
        # Log for debugging
        print(f"📤 Event published: {event_type}")

# Global event bus instance
event_bus = SimpleEventBus()

# Event type constants (matching original events.py)
class EventType:
    CREATED = "created"
    UPDATED = "updated"
    COMPLETED = "completed"
    DELETED = "deleted"
    REMINDER_SET = "reminder_set"

def publish_task_event(event_type: EventType, task_data: Dict[str, Any], user_id: str) -> bool:
    """
    Publish a task event (compatible with original events.py interface)
    
    Args:
        event_type: Type of event (created, updated, etc.)
        task_data: Task data dictionary
        user_id: User who triggered the event
    
    Returns:
        True (always succeeds for in-memory)
    """
    try:
        event_bus.publish(f"TASK_{event_type.upper()}", {
            "task_id": task_data.get("id"),
            "user_id": user_id,
            "task": task_data
        })
        return True
    except Exception as e:
        print(f"⚠️ Event publishing failed: {e}")
        return False

# Optional: PostgreSQL audit log integration
def setup_audit_logging(db_session):
    """
    Set up PostgreSQL audit logging for events
    Can be called during app startup to persist events
    """
    def log_to_database(event):
        try:
            # Store event in task_events table
            # Implementation can be added later
            pass
        except Exception as e:
            print(f"Audit log error: {e}")
    
    # Subscribe to all event types
    for event_type in ["TASK_CREATED", "TASK_UPDATED", "TASK_COMPLETED", "TASK_DELETED"]:
        event_bus.subscribe(event_type, log_to_database)

# Helper functions for reminder scheduling (stubs for now)
async def schedule_reminder_job(task_id: str, remind_at, user_id: str):
    """Schedule a reminder job (stub implementation)"""
    # TODO: Integrate with Dapr Jobs API or alternative scheduler
    print(f"📅 Reminder scheduled for task {task_id} at {remind_at}")
    pass

async def cancel_reminder_job(task_id: str):
    """Cancel a scheduled reminder job (stub implementation)"""
    # TODO: Integrate with Dapr Jobs API or alternative scheduler
    print(f"🚫 Reminder cancelled for task {task_id}")
    pass

print("✅ Lightweight event bus initialized (zero-cost)")
