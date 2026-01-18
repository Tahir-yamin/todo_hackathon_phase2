"""MCP Server for Todo App - Tool Definitions with OpenRouter"""
from typing import Optional, List
from datetime import datetime
import uuid
from sqlmodel import Session, select
from models import Task, User
from db import get_session

# Phase 5: Import lightweight event publishing
try:
    from simple_events import publish_task_event, EventType
    EVENTS_ENABLED = True
    print("✅ Lightweight event bus loaded")
except ImportError:
    print("⚠️ Events module not available - running without event publishing")
    EVENTS_ENABLED = False

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
                            },
                            # Phase 5: New fields
                            "due_date": {
                                "type": "string",
                                "format": "date-time",
                                "description": "Due date in ISO format (e.g., 2026-01-10T14:00:00)"
                            },
                            "remind_at": {
                                "type": "string",
                                "format": "date-time",
                                "description": "When to send reminder (ISO format)"
                            },
                            "recurrence_type": {
                                "type": "string",
                                "enum": ["NONE", "DAILY", "WEEKLY", "MONTHLY", "YEARLY"],
                                "description": "Recurrence pattern for recurring tasks"
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
                            },
                            # Phase 5: Advanced filters
                            "due_before": {
                                "type": "string",
                                "format": "date-time",
                                "description": "Filter tasks due before this date"
                            },
                            "due_after": {
                                "type": "string",
                                "format": "date-time",
                                "description": "Filter tasks due after this date"
                            },
                            "has_recurrence": {
                                "type": "boolean",
                                "description": "Filter recurring tasks only"
                            },
                            "sort_by": {
                                "type": "string",
                                "enum": ["created_at", "due_date", "priority", "title"],
                                "description": "Sort results by field"
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
                            },
                            # Phase 5: New update fields
                            "due_date": {
                                "type": "string",
                                "format": "date-time",
                                "description": "New due date"
                            },
                            "remind_at": {
                                "type": "string",
                                "format": "date-time",
                                "description": "New reminder time"
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
            },
            {
                "type": "function",
                "function": {
                    "name": "bulk_delete_tasks",
                    "description": "Delete multiple tasks at once. Use this when user asks to 'delete all tasks', 'delete open tasks', 'delete completed tasks', or similar bulk delete operations. Can filter by status, priority, or category.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "status": {
                                "type": "string",
                                "enum": ["todo", "in_progress", "completed"],
                                "description": "Filter: only delete tasks with this status. 'Open tasks' means status='todo' or 'in_progress'"
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["low", "medium", "high"],
                                "description": "Filter: only delete tasks with this priority"
                            },
                            "category": {
                                "type": "string",
                                "description": "Filter: only delete tasks with this category"
                            }
                        }
                    }
                }
            },
            # Phase 5: New tool for reminders
            {
                "type": "function",
                "function": {
                    "name": "set_reminder",
                    "description": "Set a reminder for a task. The user will be notified at the specified time.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "string",
                                "description": "ID of the task to set reminder for"
                            },
                            "remind_at": {
                                "type": "string",
                                "format": "date-time",
                                "description": "When to send the reminder (ISO format)"
                            }
                        },
                        "required": ["task_id", "remind_at"]
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
            elif tool_name == "bulk_delete_tasks":
                return await self._bulk_delete_tasks(session, arguments, user_id)
            elif tool_name == "set_reminder":
                return await self._set_reminder(session, arguments, user_id)
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
            # Parse datetime fields
            due_date = None
            if args.get("due_date"):
                due_date = datetime.fromisoformat(args["due_date"].replace("Z", "+00:00"))
            
            remind_at = None
            if args.get("remind_at"):
                remind_at = datetime.fromisoformat(args["remind_at"].replace("Z", "+00:00"))
            
            task = Task(
                id=str(uuid.uuid4()),
                user_id=user_id,
                title=args["title"],
                description=args.get("description", ""),
                priority=args.get("priority", "medium"),
                category=args.get("category", "Personal"),
                status="todo",
                due_date=due_date,
                remind_at=remind_at,
                recurrence_type=args.get("recurrence_type"),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            session.add(task)
            session.commit()
            session.refresh(task)
            
            print(f"✅ Created task: {task.title} (ID: {task.id})")
            
            # Phase 5: Publish event
            if EVENTS_ENABLED:
                await publish_task_event(
                    EventType.CREATED,
                    {"id": task.id, "title": task.title, "priority": task.priority},
                    user_id
                )
                
                # Schedule reminder if set
                if remind_at:
                    await schedule_reminder_job(task.id, remind_at, user_id)
            
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
            
            
            # Phase 5: Advanced filters (skip if columns don't exist)
            try:
                if args.get("due_before"):
                    due_before = datetime.fromisoformat(args["due_before"].replace("Z", "+00:00"))
                    statement = statement.where(Task.due_date <= due_before)
                if args.get("due_after"):
                    due_after = datetime.fromisoformat(args["due_after"].replace("Z", "+00:00"))
                    statement = statement.where(Task.due_date >= due_after)
                if args.get("has_recurrence"):
                    statement = statement.where(Task.recurrence_type != None)
            except AttributeError:
                # Phase 5 columns don't exist in database, skip advanced filters
                pass
            
            # Phase 5: Sorting
            sort_by = args.get("sort_by", "created_at")
            if hasattr(Task, sort_by):
                sort_col = getattr(Task, sort_by)
                statement = statement.order_by(sort_col.desc())
            
            tasks = session.exec(statement).all()
            
            task_list = [
                {
                    "id": t.id,
                    "title": t.title,
                    "description": t.description,
                    "priority": t.priority,
                    "status": t.status,
                    "category": t.category,
                    "due_date": t.due_date.isoformat() if t.due_date else None,
                    "remind_at": t.remind_at.isoformat() if t.remind_at else None,
                    "recurrence": t.recurrence if hasattr(t, 'recurrence') else "NONE",
                    "next_occurrence": t.next_occurrence.isoformat() if hasattr(t, 'next_occurrence') and t.next_occurrence else None,
                    "created_at": t.created_at.isoformat() if t.created_at else None
                }
                for t in tasks
            ]
            
            # Format as markdown table for chat display
            if tasks:
                markdown_table = "| Title | Priority | Status | Due Date |\\n"
                markdown_table += "|-------|----------|--------|----------|\\n"
                for t in tasks:
                    title = t.title[:30] + "..." if len(t.title) > 30 else t.title
                    due_date = t.due_date if hasattr(t, 'due_date') else None
                    due = due_date.strftime("%b %d") if due_date else "N/A"
                    markdown_table += f"| {title} | {t.priority} | {t.status} | {due} |\\n"
                formatted_message = f"Found {len(tasks)} task(s):\\n\\n{markdown_table}"
            else:
                formatted_message = "You have no tasks at the moment."
            
            print(f"✅ Listed {len(task_list)} tasks")
            
            return {
                "success": True,
                "count": len(task_list),
                "tasks": task_list,
                "formatted_output": formatted_message
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
            
            # Parse datetime fields
            if "due_date" in args and args["due_date"]:
                args["due_date"] = datetime.fromisoformat(args["due_date"].replace("Z", "+00:00"))
            if "remind_at" in args and args["remind_at"]:
                args["remind_at"] = datetime.fromisoformat(args["remind_at"].replace("Z", "+00:00"))
            
            # Update fields
            for key, value in args.items():
                if hasattr(task, key) and value is not None:
                    setattr(task, key, value)
            
            task.updated_at = datetime.utcnow()
            session.add(task)
            session.commit()
            session.refresh(task)
            
            print(f"✅ Updated task: {task.title}")
            
            # Phase 5: Publish event
            if EVENTS_ENABLED:
                await publish_task_event(
                    EventType.UPDATED,
                    {"id": task.id, "title": task.title, "status": task.status},
                    user_id
                )
                
                # Update reminder if changed
                if task.remind_at:
                    await cancel_reminder_job(task.id)
                    await schedule_reminder_job(task.id, task.remind_at, user_id)
            
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
            
            # Phase 5: Publish event and cancel reminder
            if EVENTS_ENABLED:
                await publish_task_event(
                    EventType.DELETED,
                    {"id": task_id, "title": title},
                    user_id
                )
                await cancel_reminder_job(task_id)
            
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
            
            # Phase 5: Publish events for each completed task
            if EVENTS_ENABLED:
                for task in tasks:
                    await publish_task_event(
                        EventType.COMPLETED,
                        {"id": task.id, "title": task.title},
                        user_id
                    )
            
            return {
                "success": True,
                "count": len(tasks),
                "message": f"Successfully marked {len(tasks)} tasks as completed"
            }
        except Exception as e:
            session.rollback()
            raise
    
    async def _bulk_delete_tasks(self, session: Session, args: dict, user_id: str) -> dict:
        """Delete multiple tasks based on filters"""
        try:
            # Build query for tasks to delete
            statement = select(Task).where(Task.user_id == user_id)
            
            # Apply filters
            if args.get("status"):
                statement = statement.where(Task.status == args["status"])
            if args.get("priority"):
                statement = statement.where(Task.priority == args["priority"])
            if args.get("category"):
                statement = statement.where(Task.category == args["category"])
            
            # If no filters specified and user says "open tasks", default to todo + in_progress
            # This is handled by the AI system prompt telling it to use status filter
            
            tasks = session.exec(statement).all()
            
            if len(tasks) == 0:
                return {
                    "success": True,
                    "count": 0,
                    "message": "No tasks matched the criteria to delete"
                }
            
            # Store task info before deletion for event publishing
            task_info = [{"id": t.id, "title": t.title} for t in tasks]
            
            # Delete all matched tasks
            for task in tasks:
                session.delete(task)
            
            session.commit()
            
            print(f"✅ Bulk deleted {len(tasks)} tasks for user {user_id}")
            
            # Phase 5: Publish events and cancel reminders for deleted tasks
            if EVENTS_ENABLED:
                for info in task_info:
                    await publish_task_event(
                        EventType.DELETED,
                        info,
                        user_id
                    )
                    await cancel_reminder_job(info["id"])
            
            # Build descriptive message based on filters
            filter_desc = []
            if args.get("status"):
                filter_desc.append(f"status '{args['status']}'")
            if args.get("priority"):
                filter_desc.append(f"{args['priority']} priority")
            if args.get("category"):
                filter_desc.append(f"category '{args['category']}'")
            
            filter_text = " with " + ", ".join(filter_desc) if filter_desc else ""
            
            return {
                "success": True,
                "count": len(tasks),
                "message": f"Successfully deleted {len(tasks)} task(s){filter_text}"
            }
        except Exception as e:
            session.rollback()
            raise
    
    async def _set_reminder(self, session: Session, args: dict, user_id: str) -> dict:
        """Set a reminder for a task (Phase 5)"""
        try:
            task_id = args["task_id"]
            remind_at_str = args["remind_at"]
            remind_at = datetime.fromisoformat(remind_at_str.replace("Z", "+00:00"))
            
            task = session.get(Task, task_id)
            
            if not task:
                return {"success": False, "error": f"Task with ID {task_id} not found"}
            
            if task.user_id != user_id:
                return {"success": False, "error": "Unauthorized: Task belongs to another user"}
            
            # Update task with reminder
            task.remind_at = remind_at
            task.updated_at = datetime.utcnow()
            session.add(task)
            session.commit()
            session.refresh(task)
            
            print(f"✅ Set reminder for task: {task.title} at {remind_at}")
            
            # Schedule reminder via Dapr Jobs API
            if EVENTS_ENABLED:
                await cancel_reminder_job(task_id)  # Cancel existing
                await schedule_reminder_job(task_id, remind_at, user_id)
                await publish_task_event(
                    EventType.REMINDER_SET,
                    {"id": task.id, "title": task.title, "remind_at": remind_at_str},
                    user_id
                )
            
            return {
                "success": True,
                "task_id": task.id,
                "remind_at": remind_at.isoformat(),
                "message": f"Reminder set for '{task.title}' at {remind_at.strftime('%B %d, %Y at %I:%M %p')}"
            }
        except Exception as e:
            session.rollback()
            raise


# Global MCP server instance
mcp = MCPServer()

