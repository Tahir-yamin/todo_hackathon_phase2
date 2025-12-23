from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional
from sqlmodel import Session, select, text
from datetime import datetime

from db import get_session
from models import Task, TaskCreate, TaskUpdate

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

def ensure_demo_user(session: Session, user_id: str):
    """
    Ensure the demo user exists in the database to prevent Foreign Key errors.
    Uses raw SQL to avoid import issues with the User model.
    """
    try:
        # Check if user exists using raw SQL for safety
        statement = text("SELECT id FROM user WHERE id = :user_id")
        result = session.exec(statement, params={"user_id": user_id}).first()
        
        if not result:
            print(f"🔧 Creating demo user: {user_id}")
            # Insert demo user
            insert_stmt = text("""
                INSERT INTO user (id, email, name, "emailVerified", "createdAt", "updatedAt")
                VALUES (:id, :email, :name, :verified, :created, :updated)
            """)
            session.exec(insert_stmt, params={
                "id": user_id,
                "email": "demo@hackathon.com",
                "name": "Hackathon Demo User",
                "verified": False,
                "created": datetime.utcnow(),
                "updated": datetime.utcnow()
            })
            session.commit()
            print(f"✅ Demo user created: {user_id}")
    except Exception as e:
        print(f"⚠️ Warning: Could not ensure user exists (might be OK if no FK constraint): {e}")
        # Continue execution - do not crash
        pass

@router.get("/")
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
    user_id = "hackathon-demo-user"
    ensure_demo_user(session, user_id)
    
    query = select(Task).where(Task.user_id == user_id)

    if status and status != "all":
        query = query.where(Task.status == status)
    if priority and priority != "all":
        query = query.where(Task.priority == priority)
    if search:
        query = query.where(Task.title.contains(search))

    # Apply sorting
    if order == "desc":
        query = query.order_by(getattr(Task, sort).desc())
    else:
        query = query.order_by(getattr(Task, sort).asc())

    # Pagination
    offset = (page - 1) * limit
    tasks = session.exec(query.offset(offset).limit(limit)).all()
    
    return {"success": True, "data": {"tasks": tasks}}

@router.post("/")
def create_task(
    task_data: TaskCreate,
    session: Session = Depends(get_session)
):
    user_id = "hackathon-demo-user"
    ensure_demo_user(session, user_id)
    
    task = Task(**task_data.dict(), user_id=user_id)
    session.add(task)
    session.commit()
    session.refresh(task)
    
    return {"success": True, "data": task, "message": "Task created successfully"}

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
