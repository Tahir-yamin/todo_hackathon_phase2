from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from sqlmodel import Session, select
from datetime import datetime

from db import get_session
from models import Task, TaskCreate, TaskUpdate, TaskPublic
from auth import get_current_user, BetterAuthUser

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

@router.get("/", response_model=dict)
def list_tasks(
    current_user: BetterAuthUser = Depends(get_current_user),
    session: Session = Depends(get_session),
    status: Optional[str] = Query(None, regex=r'^(all|todo|in_progress|completed)$'),
    priority: Optional[str] = Query(None, regex=r'^(all|low|medium|high)$'),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    sort: str = Query("created_at"),
    order: str = Query("desc")
):
    """
    Retrieve all tasks for the authenticated user with optional filtering and pagination.
    """
    # Build the query
    query = select(Task).where(Task.user_id == current_user.id)

    # Apply filters
    if status and status != "all":
        query = query.where(Task.status == status)

    if priority and priority != "all":
        query = query.where(Task.priority == priority)

    if search:
        query = query.where(Task.title.contains(search) | Task.description.contains(search))

    # Apply sorting
    if sort == "created_at":
        if order == "desc":
            query = query.order_by(Task.created_at.desc())
        else:
            query = query.order_by(Task.created_at.asc())
    elif sort == "due_date":
        if order == "desc":
            query = query.order_by(Task.due_date.desc())
        else:
            query = query.order_by(Task.due_date.asc())
    elif sort == "priority":
        if order == "desc":
            query = query.order_by(Task.priority.desc())
        else:
            query = query.order_by(Task.priority.asc())

    # Calculate pagination
    offset = (page - 1) * limit
    query = query.offset(offset).limit(limit)

    # Execute query
    tasks = session.exec(query).all()

    # Count total for pagination metadata
    count_query = select(Task).where(Task.user_id == current_user.id)
    if status and status != "all":
        count_query = count_query.where(Task.status == status)
    if priority and priority != "all":
        count_query = count_query.where(Task.priority == priority)
    if search:
        count_query = count_query.where(Task.title.contains(search) | Task.description.contains(search))

    total = len(session.exec(count_query).all())

    return {
        "success": True,
        "data": {
            "tasks": tasks,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "total_pages": (total + limit - 1) // limit
            }
        }
    }


@router.post("/", response_model=dict)
def create_task(
    task_data: TaskCreate,
    current_user: BetterAuthUser = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.
    """
    # Create task instance with user_id
    task = Task(
        **task_data.dict(),
        user_id=current_user.id  # Now both are strings
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    return {
        "success": True,
        "data": task,
        "message": "Task created successfully"
    }


@router.get("/{id}", response_model=dict)
def get_task(
    id: str,  # Changed from uuid.UUID to str
    current_user: BetterAuthUser = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Retrieve a specific task by ID.
    """
    task = session.get(Task, id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Verify that the task belongs to the current user
    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this task")

    return {
        "success": True,
        "data": task
    }


@router.put("/{id}", response_model=dict)
def update_task(
    id: str,  # Changed from uuid.UUID to str
    task_data: TaskUpdate,
    current_user: BetterAuthUser = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a specific task.
    """
    task = session.get(Task, id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Verify that the task belongs to the current user
    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this task")

    # Update task fields
    task_dict = task_data.dict(exclude_unset=True)
    for key, value in task_dict.items():
        setattr(task, key, value)

    # Update the updated_at timestamp
    task.updated_at = datetime.utcnow()

    # Handle status change to completed
    if task_data.status == "completed" and task.status != "completed":
        task.completed_at = datetime.utcnow()
    elif task_data.status in ["todo", "in_progress"] and task.status == "completed":
        task.completed_at = None

    session.add(task)
    session.commit()
    session.refresh(task)

    return {
        "success": True,
        "data": task,
        "message": "Task updated successfully"
    }


@router.delete("/{id}", response_model=dict)
def delete_task(
    id: str,
    current_user: BetterAuthUser = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task.
    """
    # Find task by ID and verify ownership
    task = session.exec(
        select(Task).where(Task.id == id).where(Task.user_id == current_user.id)
    ).first()
    
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found or you don't have permission to delete it"
        )
    
    session.delete(task)
    session.commit()
    
    return {
        "success": True,
        "message": f"Task '{task.title}' deleted successfully"
    }
