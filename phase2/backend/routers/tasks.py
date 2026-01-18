from fastapi import APIRouter, HTTPException, Depends, Query, Header
from typing import Optional
from sqlmodel import Session, select
from datetime import datetime
import traceback

from db import get_session
from models import Task, TaskCreate, TaskUpdate, User  # Import User model

# Phase 5: Kafka event publishing
from kafka_producer import (
    publish_task_created,
    publish_task_updated,
    publish_task_deleted,
    publish_task_completed
)

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

def ensure_demo_user(session: Session, user_id: str) -> User:
    """
    Ensure the demo user exists using pure SQLModel ORM.
    No raw SQL - type-safe, database-agnostic.
    """
    try:
        # Check if user exists using ORM
        user = session.get(User, user_id)
        
        if not user:
            print(f"🔧 Creating demo user: {user_id}")
            # Create user using ORM
            user = User(
                id=user_id,
                email="demo@hackathon.com",
                name="Hackathon Demo User",
                emailVerified=False,
                createdAt=datetime.utcnow(),
                updatedAt=datetime.utcnow()
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            print(f"✅ Demo user created: {user_id}")
        
        return user
    
    except Exception as e:
        print(f"❌ Error creating demo user: {e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to create demo user: {str(e)}"
        )

@router.get("")
def list_tasks(
    session: Session = Depends(get_session),
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1),
    limit: int = Query(10),
    sort: str = Query("created_at"),
    order: str = Query("desc"),
    x_user_id: Optional[str] = Header(None)
):
    try:
        # Use header user_id if provided, otherwise fall back to demo user
        user_id = x_user_id if x_user_id else "hackathon-demo-user"
        # BetterAuth handles user creation - no need to manually ensure user exists
       # ensure_demo_user(session, user_id)
        
        query = select(Task).where(Task.user_id == user_id)

        if status and status != "all":
            query = query.where(Task.status == status)
        if priority and priority != "all":
            query = query.where(Task.priority == priority)
        if search:
            query = query.where(Task.title.contains(search))

        if order == "desc":
            query = query.order_by(getattr(Task, sort).desc())
        else:
            query = query.order_by(getattr(Task, sort).asc())

        offset = (page - 1) * limit
        tasks = session.exec(query.offset(offset).limit(limit)).all()
        
        return {"success": True, "data": {"tasks": tasks}}
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"\n{'='*60}")
        print(f"❌ ERROR in list_tasks")
        print(f"Error: {str(e)}")
        print(f"Traceback:\n{error_details}")
        print(f"{'='*60}\n")
        raise HTTPException(status_code=500, detail=f"Task list error: {str(e)}")

@router.post("")
def create_task(
    task_data: TaskCreate,
    session: Session = Depends(get_session),
    x_user_id: Optional[str] = Header(None)
):
    try:
        # Use header user_id if provided, otherwise fall back to demo user
        user_id = x_user_id if x_user_id else "hackathon-demo-user"
        # BetterAuth handles user creation
        # ensure_demo_user(session, user_id)
        
        task = Task(**task_data.dict(), user_id=user_id)
        session.add(task)
        session.commit()
        session.refresh(task)
        
        # Phase 5: Publish Kafka event
        publish_task_created(task.dict())
        
        return {"success": True, "data": task, "message": "Task created successfully"}
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"\n{'='*60}")
        print(f"❌ ERROR in create_task")
        print(f"Error: {str(e)}")
        print(f"Traceback:\n{error_details}")
        print(f"{'='*60}\n")
        raise HTTPException(status_code=500, detail=f"Task creation error: {str(e)}")

@router.put("/{id}")
def update_task(
    id: str,
    task_data: TaskUpdate,
    session: Session = Depends(get_session)
):
    task = session.get(Task, id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    task_dict = task_data.dict(exclude_unset=True)
    for key, value in task_dict.items():
        setattr(task, key, value)
        
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    
    # Phase 5: Publish Kafka event
    publish_task_updated(task.dict())
    
    return {"success": True, "data": task}

@router.delete("/{id}")
def delete_task(
    id: str,
    session: Session = Depends(get_session)
):
    task = session.get(Task, id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Store task data before deletion for event publishing
    task_id = task.id
    user_id = task.user_id
    
    session.delete(task)
    session.commit()
    
    # Phase 5: Publish Kafka event
    publish_task_deleted(task_id, user_id)
    
    return {"success": True, "message": "Task deleted"}

@router.post("/{id}/complete")
def complete_task(
    id: str,
    session: Session = Depends(get_session)
):
    """Mark task as complete - triggers recurring task creation via Kafka"""
    task = session.get(Task, id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Mark as completed
    task.status = "completed"
    task.updated_at = datetime.utcnow()
    
    session.add(task)
    session.commit()
    session.refresh(task)
    
    # Phase 5: Publish event (recurring service will handle next occurrence)
    publish_task_completed(task.dict())
    
    return {"success": True, "data": task, "message": "Task completed"}


@router.post("/bulk-complete")
def bulk_complete_tasks(
    session: Session = Depends(get_session),
    x_user_id: Optional[str] = Header(None)
):
    """Complete all incomplete tasks for the user"""
    try:
        # Use header user_id if provided, otherwise fall back to demo user
        user_id = x_user_id if x_user_id else "hackathon-demo-user"
        
        # Get all incomplete tasks for this user
        statement = select(Task).where(
            Task.user_id == user_id,
            Task.status != "completed"
        )
        tasks = session.exec(statement).all()
        
        # Mark each as completed
        for task in tasks:
            task.status = "completed"
            task.updated_at = datetime.utcnow()
            session.add(task)
        
        session.commit()
        
        print(f"✅ Bulk completed {len(tasks)} tasks for user {user_id}")
        
        return {
            "success": True,
            "count": len(tasks),
            "message": f"Marked {len(tasks)} tasks as completed"
        }
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"\n{'='*60}")
        print(f"❌ ERROR in bulk_complete_tasks")
        print(f"Error: {str(e)}")
        print(f"Traceback:\n{error_details}")
        print(f"{'='*60}\n")
        raise HTTPException(status_code=500, detail=f"Bulk complete error: {str(e)}")
