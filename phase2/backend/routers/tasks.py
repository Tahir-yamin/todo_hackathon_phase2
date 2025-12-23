from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional
from sqlmodel import Session, select
from datetime import datetime
import traceback

from db import get_session
from models import Task, TaskCreate, TaskUpdate, User  # Import User model

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
    order: str = Query("desc")
):
    try:
        user_id = "hackathon-demo-user"
        # Ensure user exists before query to prevent issues
        ensure_demo_user(session, user_id)
        
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
    session: Session = Depends(get_session)
):
    try:
        user_id = "hackathon-demo-user"
        ensure_demo_user(session, user_id)
        
        task = Task(**task_data.dict(), user_id=user_id)
        session.add(task)
        session.commit()
        session.refresh(task)
        
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
    
    return {"success": True, "data": task}

@router.delete("/{id}")
def delete_task(
    id: str,
    session: Session = Depends(get_session)
):
    task = session.get(Task, id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    session.delete(task)
    session.commit()
    
    return {"success": True, "message": "Task deleted"}
