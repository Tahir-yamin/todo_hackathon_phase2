"""
Gemini AI Function Calling Tools for Task Management

This module defines the function declarations and execution logic
for Google Gemini to manage TODO tasks via natural language.
"""

import os
from typing import Optional
from datetime import datetime
from sqlmodel import Session, select
from backend.models import Task

# Gemini function declarations
task_functions = [
    {
        "name": "add_task",
        "description": "Create a new task in the user's TODO list",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The title of the task"
                },
                "description": {
                    "type": "string",
                    "description": "Optional description of the task"
                },
                "priority": {
                    "type": "string",
                    "enum": ["low", "medium", "high"],
                    "description": "Priority level of the task"
                }
            },
            "required": ["title"]
        }
    },
    {
        "name": "list_tasks",
        "description": "Get all tasks from the user's TODO list",
        "parameters": {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": ["all", "todo", "in_progress", "completed"],
                    "description": "Filter tasks by status"
                }
            }
        }
    },
    {
        "name": "complete_task",
        "description": "Mark a specific task as completed",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "integer",
                    "description": "The ID of the task to complete"
                }
            },
            "required": ["task_id"]
        }
    },
    {
        "name": "delete_task",
        "description": "Delete a task from the TODO list",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "integer",
                    "description": "The ID of the task to delete"
                }
            },
            "required": ["task_id"]
        }
    },
    {
        "name": "update_task",
        "description": "Update a task's title or description",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "integer",
                    "description": "The ID of the task to update"
                },
                "title": {
                    "type": "string",
                    "description": "New title for the task"
                },
                "description": {
                    "type": "string",
                    "description": "New description for the task"
                }
            },
            "required": ["task_id"]
        }
    }
]


async def execute_function(function_name: str, args: dict, user_id: str, db: Session) -> dict:
    """
    Execute the requested Gemini function
    
    Args:
        function_name: Name of the function to execute
        args: Arguments passed by Gemini
        user_id: ID of the user making the request
        db: Database session
        
    Returns:
        dict: Result of the function execution
    """
    
    try:
        if function_name == "add_task":
            # Create new task
            task = Task(
                user_id=user_id,
                title=args["title"],
                description=args.get("description", ""),
                priority=args.get("priority", "medium"),
                status="todo"
            )
            db.add(task)
            db.commit()
            db.refresh(task)
            
            return {
                "success": True,
                "task_id": task.id,
                "status": "created",
                "title": task.title,
                "priority": task.priority
            }
        
        elif function_name == "list_tasks":
            # Get all tasks with optional status filter
            status_filter = args.get("status", "all")
            query = select(Task).where(Task.user_id == user_id)
            
            if status_filter != "all":
                query = query.where(Task.status == status_filter)
            
            tasks = db.exec(query).all()
            
            return {
                "success": True,
                "count": len(tasks),
                "tasks": [
                    {
                        "id": t.id,
                        "title": t.title,
                        "status": t.status,
                        "priority": t.priority,
                        "completed": t.status == "completed"
                    }
                    for t in tasks
                ]
            }
        
        elif function_name == "complete_task":
            # Mark task as completed
            task_id = args["task_id"]
            task = db.exec(
                select(Task).where(Task.id == task_id, Task.user_id == user_id)
            ).first()
            
            if task:
                task.status = "completed"
                task.completed_at = datetime.utcnow()
                task.updated_at = datetime.utcnow()
                db.commit()
                
                return {
                    "success": True,
                    "task_id": task.id,
                    "status": "completed",
                    "title": task.title
                }
            
            return {
                "success": False,
                "error": f"Task {task_id} not found"
            }
        
        elif function_name == "delete_task":
            # Delete task
            task_id = args["task_id"]
            task = db.exec(
                select(Task).where(Task.id == task_id, Task.user_id == user_id)
            ).first()
            
            if task:
                title = task.title
                db.delete(task)
                db.commit()
                
                return {
                    "success": True,
                    "task_id": task_id,
                    "status": "deleted",
                    "title": title
                }
            
            return {
                "success": False,
                "error": f"Task {task_id} not found"
            }
        
        elif function_name == "update_task":
            # Update task
            task_id = args["task_id"]
            task = db.exec(
                select(Task).where(Task.id == task_id, Task.user_id == user_id)
            ).first()
            
            if task:
                if "title" in args:
                    task.title = args["title"]
                if "description" in args:
                    task.description = args["description"]
                
                task.updated_at = datetime.utcnow()
                db.commit()
                
                return {
                    "success": True,
                    "task_id": task.id,
                    "status": "updated",
                    "title": task.title
                }
            
            return {
                "success": False,
                "error": f"Task {task_id} not found"
            }
        
        else:
            return {
                "success": False,
                "error": f"Unknown function: {function_name}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
