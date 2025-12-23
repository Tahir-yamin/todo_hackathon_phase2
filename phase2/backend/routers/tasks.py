from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional
from sqlmodel import Session, select, text
from datetime import datetime

from db import get_session
from models import Task, TaskCreate, TaskUpdate

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

def ensure_demo_user(session: Session, user_id: str):
    """
    Ensure the demo user exists in the database.
    Uses raw SQL with QUOTED table names to support Postgres.
    """
    try:
        # Check if user exists (quote "user" table - it's a reserved keyword!)
        statement = text('SELECT id FROM "user" WHERE id = :user_id')
        result = session.exec(statement, params={"user_id": user_id}).first()
        
        if not result:
            print(f"🔧 Creating demo user: {user_id}")
            # Insert demo user (Note the quotes around "user" and columns)
            insert_stmt = text("""
                INSERT INTO "user" (id, email, name, "emailVerified", "createdAt", "updatedAt")
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
        print(f"⚠️ Warning: Demo user creation failed (table='user'): {e}")
        # If the table is actually named 'users' (plural), try that as fallback
        try:
            # Fallback for 'users' table name
            statement = text('SELECT id FROM users WHERE id = :user_id')
            result = session.exec(statement, params={"user_id": user_id}).first()
            if not result:
                print(f"🔧 Creating demo user in 'users' table: {user_id}")
                insert_stmt = text("""
                    INSERT INTO users (id, email, name, "emailVerified", "createdAt", "updatedAt")
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
                print(f"✅ Demo user created in 'users' table: {user_id}")
        except Exception as e2:
            print(f"⚠️ Critical: Could not create user in 'user' or 'users' table. DB Error: {e2}")

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
