"""
PostgreSQL Audit Logging for Phase 5
Zero-cost event persistence using existing database
"""

from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import Optional
from datetime import datetime
import json

class TaskEventLog(SQLModel, table=True):
    """Audit log table for all task events"""
    __tablename__ = "task_events"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    event_type: str = Field(index=True)  # TASK_CREATED, TASK_UPDATED, etc.
    task_id: Optional[str] = Field(index=True)
    user_id: Optional[str] = Field(index=True)
    event_data: str  # JSON string of event data
    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True)
    
    class Config:
        json_schema_extra = {
            "example": {
                "event_type": "TASK_CREATED",
                "task_id": "abc-123",
                "user_id": "user-456",
                "event_data": '{"title": "Test task"}',
                "timestamp": "2026-01-17T23:00:00"
            }
        }


def setup_audit_logging(database_url: str, event_bus):
    """
    Setup PostgreSQL audit logging for event persistence
    
    Args:
        database_url: PostgreSQL connection string
        event_bus: SimpleEventBus instance to subscribe to
    """
    from sqlmodel import create_engine
    
    engine = create_engine(database_url)
    
    # Create table if it doesn't exist
    TaskEventLog.metadata.create_all(engine)
    print("✅ Audit logging table created/verified")
    
    def log_event_to_db(event: dict):
        """Log event to PostgreSQL"""
        try:
            with Session(engine) as session:
                log_entry = TaskEventLog(
                    event_type=event.get("event_type", "UNKNOWN"),
                    task_id=event.get("data", {}).get("task_id"),
                    user_id=event.get("data", {}).get("user_id"),
                    event_data=json.dumps(event.get("data", {})),
                    timestamp=datetime.fromisoformat(event["timestamp"]) if "timestamp" in event else datetime.utcnow()
                )
                session.add(log_entry)
                session.commit()
                print(f"📝 Logged {event.get('event_type')} to audit table")
        except Exception as e:
            print(f"⚠️ Audit log error: {e}")
    
    # Subscribe to all event types
    for event_type in ["TASK_CREATED", "TASK_UPDATED", "TASK_COMPLETED", "TASK_DELETED"]:
        event_bus.subscribe(event_type, log_event_to_db)
    
    print("✅ Audit logging subscribed to all events")
    return TaskEventLog


def query_audit_log(database_url: str, task_id: Optional[str] = None, 
                   user_id: Optional[str] = None, limit: int = 100):
    """
    Query audit log for task history
    
    Args:
        database_url: PostgreSQL connection string
        task_id: Optional filter by task ID
        user_id: Optional filter by user ID
        limit: Max records to return
    
    Returns:
        List of audit log entries
    """
    engine = create_engine(database_url)
    
    with Session(engine) as session:
        statement = select(TaskEventLog)
        
        if task_id:
            statement = statement.where(TaskEventLog.task_id == task_id)
        if user_id:
            statement = statement.where(TaskEventLog.user_id == user_id)
        
        statement = statement.order_by(TaskEventLog.timestamp.desc()).limit(limit)
        
        results = session.exec(statement).all()
        return results


# Example usage:
# from audit_logging import setup_audit_logging
# from simple_events import event_bus
# import os
# 
# setup_audit_logging(os.getenv("DATABASE_URL"), event_bus)
# Now all events are automatically logged to PostgreSQL!
