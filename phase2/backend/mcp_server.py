"""MCP Server for Todo App - Tool Definitions with OpenRouter"""
from typing import Optional, List
from datetime import datetime
import uuid
from sqlmodel import Session, select
from models import Task, User
from db import get_session

class MCPServer:
    """Model Context Protocol server for task management"""
    
    def get_tools_schema(self) -> List[dict]:
        """Return OpenAI-compatible tool schemas for function calling"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Create a new task in the todo list",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "Task title (required)"
                            },
                            "description": {
                                "type": "string",
                                "description": "Detailed task description"
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["low", "medium", "high"],
                                "description": "Task priority level"
                            },
                            "category": {
                                "type": "string",
                                "description": "Task category (e.g., work, personal, shopping)"
                            }
                        },
                        "required": ["title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "List tasks. IMPORTANT: By default, show only PENDING tasks (status='todo' or 'in_progress'). Only show 'completed' tasks if the user explicitly asks for 'all tasks', 'completed tasks', 'finished tasks', or 'history'.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "status": {
                                "type": "string",
                                "enum": ["todo", "in_progress", "completed"],
                                "description": "Filter by task status. Default to 'todo' for pending tasks"
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["low", "medium", "high"],
                                "description": "Filter by priority level"
                            },
                            "category": {
                                "type": "string",
                                "description": "Filter by category"
                            }
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Update an existing task by ID",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "string",
                                "description": "Unique ID of the task to update"
                            },
                            "title": {
                                "type": "string",
                                "description": "New task title"
                            },
                            "status": {
                                "type": "string",
                                "enum": ["todo", "in_progress", "completed"],
                                "description": "New task status"
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["low", "medium", "high"],
                                "description": "New priority level"
                            },
                            "completed": {
                                "type": "boolean",
                                "description": "Mark task as completed/incomplete"
                            }
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Delete a task permanently",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "string",
                                "description": "ID of the task to delete"
                            }
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "bulk_complete_tasks",
                    "description": "Mark ALL incomplete tasks as completed. Use this when user asks to 'complete all tasks', 'mark everything as done', or similar bulk operations.",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            }
        ]
    
    async def execute_tool(self, tool_name: str, arguments: dict, user_id: str) -> dict:
        """Execute an MCP tool with the given arguments"""
        session = next(get_session())
        
        try:
            print(f"🔧 Executing tool: {tool_name}")
            print(f"📊 Arguments: {arguments}")
            print(f"👤 User: {user_id}")
            
            if tool_name == "add_task":
                return await self._add_task(session, arguments, user_id)
            elif tool_name == "list_tasks":
                return await self._list_tasks(session, arguments, user_id)
            elif tool_name == "update_task":
                return await self._update_task(session, arguments, user_id)
            elif tool_name == "delete_task":
                return await self._delete_task(session, arguments, user_id)
            elif tool_name == "bulk_complete_tasks":
                return await self._bulk_complete_tasks(session, user_id)
            else:
                return {"success": False, "error": f"Unknown tool: {tool_name}"}
        except Exception as e:
            print(f"❌ Tool execution error: {e}")
            return {"success": False, "error": str(e)}
        finally:
            session.close()
    
    async def _add_task(self, session: Session, args: dict, user_id: str) -> dict:
        """Add a new task to the database"""
        try:
            task = Task(
                id=str(uuid.uuid4()),
                user_id=user_id,
                title=args["title"],
                description=args.get("description", ""),
                priority=args.get("priority", "medium"),
                category=args.get("category", "Personal"),
                status="todo",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            session.add(task)
            session.commit()
            session.refresh(task)
            
            print(f"✅ Created task: {task.title} (ID: {task.id})")
            
            return {
                "success": True,
                "task_id": task.id,
                "message": f"Successfully created task: '{task.title}'"
            }
        except Exception as e:
            session.rollback()
            raise
    
    async def _list_tasks(self, session: Session, args: dict, user_id: str) -> dict:
        """List tasks with optional filters"""
        try:
            statement = select(Task).where(Task.user_id == user_id)
            
            # Apply filters
            if args.get("status"):
                statement = statement.where(Task.status == args["status"])
            if args.get("priority"):
                statement = statement.where(Task.priority == args["priority"])
            if args.get("category"):
                statement = statement.where(Task.category == args["category"])
            
            tasks = session.exec(statement).all()
            
            task_list = [
                {
                    "id": t.id,
                    "title": t.title,
                    "description": t.description,
                    "priority": t.priority,
                    "status": t.status,
                    "category": t.category,
                    "created_at": t.created_at.isoformat() if t.created_at else None
                }
                for t in tasks
            ]
            
            print(f"✅ Listed {len(task_list)} tasks")
            
            return {
                "success": True,
                "count": len(task_list),
                "tasks": task_list
            }
        except Exception as e:
            raise
    
    async def _update_task(self, session: Session, args: dict, user_id: str) -> dict:
        """Update an existing task"""
        try:
            task_id = args.pop("task_id")
            task = session.get(Task, task_id)
            
            if not task:
                return {"success": False, "error": f"Task with ID {task_id} not found"}
            
            if task.user_id != user_id:
                return {"success": False, "error": "Unauthorized: Task belongs to another user"}
            
            # Handle 'completed' boolean
            if "completed" in args:
                args["status"] = "completed" if args.pop("completed") else "todo"
            
            # Update fields
            for key, value in args.items():
                if hasattr(task, key) and value is not None:
                    setattr(task, key, value)
            
            task.updated_at = datetime.utcnow()
            session.add(task)
            session.commit()
            session.refresh(task)
            
            print(f"✅ Updated task: {task.title}")
            
            return {
                "success": True,
                "task_id": task.id,
                "message": f"Successfully updated task: '{task.title}'"
            }
        except Exception as e:
            session.rollback()
            raise
    
    async def _delete_task(self, session: Session, args: dict, user_id: str) -> dict:
        """Delete a task"""
        try:
            task_id = args["task_id"]
            task = session.get(Task, task_id)
            
            if not task:
                return {"success": False, "error": f"Task with ID {task_id} not found"}
            
            if task.user_id != user_id:
                return {"success": False, "error": "Unauthorized: Task belongs to another user"}
            
            title = task.title
            session.delete(task)
            session.commit()
            
            print(f"✅ Deleted task: {title}")
            
            return {
                "success": True,
                "message": f"Successfully deleted task: '{title}'"
            }
        except Exception as e:
            session.rollback()
            raise
    
    async def _bulk_complete_tasks(self, session: Session, user_id: str) -> dict:
        """Mark all incomplete tasks as completed"""
        try:
            # Get all active tasks (both 'todo' and 'in_progress') for this user
            statement = select(Task).where(
                Task.user_id == user_id,
                Task.status.in_(["todo", "in_progress"])  # Catch all active tasks
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
                "message": f"Successfully marked {len(tasks)} tasks as completed"
            }
        except Exception as e:
            session.rollback()
            raise


# Global MCP server instance
mcp = MCPServer()
