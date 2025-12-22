"""
Gemini AI Agent for Task Management - OpenRouter + DeepSeek V3

Using OpenRouter for unlimited free tier with DeepSeek V3 model.
"""

import os
import json
from openai import OpenAI
from sqlmodel import Session, select
from backend.models import Task
from dotenv import load_dotenv
import pathlib
from datetime import datetime, timedelta

# Force load .env
env_path = pathlib.Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Initialize Client pointing to OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# Define Tools (JSON Schema for OpenAI format)
tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "create_task",
            "description": "Create a new todo task with smart extraction of due date and priority from natural language.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "The task title"},
                    "description": {"type": "string", "description": "Optional task description"},
                    "due_date": {"type": "string", "description": "YYYY-MM-DD format (calculated from 'tomorrow', 'next friday', etc)"},
                    "priority": {"type": "string", "enum": ["low", "medium", "high"], "description": "Task priority level"},
                    "category": {"type": "string", "description": "Category like work, personal, shopping, etc"}
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List all tasks for the current user",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a task by searching for a keyword in its title",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {"type": "string", "description": "The word to search for in task title (e.g., 'milk', 'groceries')"}
                },
                "required": ["keyword"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark a task as completed by searching for a keyword in its title",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {"type": "string", "description": "The word to search for in task title"}
                },
                "required": ["keyword"]
            }
        }
    }
]


async def run_agent(user_id: str, message: str, db: Session) -> str:
    """
    Run AI agent with DeepSeek V3 via OpenRouter for task management.
    
    Args:
        user_id: User ID for task operations
        message: User's message
        db: Database session
        
    Returns:
        str: Agent's text response
    """
    try:
        # System Prompt with Smart Date/Priority Extraction Instructions
        system_prompt = """You are a smart Todo Assistant with natural language understanding.

When users create tasks, automatically extract and calculate:
1. **Due Dates**: Convert natural language to YYYY-MM-DD format
   - "tomorrow" → calculate tomorrow's date
   - "next friday" → calculate next Friday's date
   - "Dec 25", "Christmas" → 2025-12-25
   - Today is {today}

2. **Priority**: Detect from keywords
   - "urgent", "important", "asap", "critical" → high
   - "later", "someday", "eventually" → low
   - default → medium

3. **Category**: Infer from context
   - "buy", "shop", "groceries" → shopping
   - "meeting", "project", "report" → work
   - "call", "family", "birthday" → personal
   - default → general

Examples:
- "Buy milk tomorrow" → title="Buy milk", due_date="2025-12-23", category="shopping"
- "Urgent: finish project report by Friday" → title="Finish project report", priority="high", due_date="2025-12-27", category="work"

Always call appropriate functions to execute user requests.
""".replace("{today}", datetime.now().strftime("%Y-%m-%d"))

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]

        # Call DeepSeek V3 via OpenRouter
        print(f"💬 Calling DeepSeek V3 for user {user_id}: {message}")
        response = client.chat.completions.create(
            model="deepseek/deepseek-chat",  # Free tier model
            messages=messages,
            tools=tools_schema,
            tool_choice="auto"
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        # Handle Tool Calls
        if tool_calls:
            for tool_call in tool_calls:
                fn_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                
                print(f"🔧 Tool called: {fn_name} with args: {args}")
                
                if fn_name == "create_task":
                    # Parse due_date if provided
                    due_date_obj = None
                    if args.get("due_date"):
                        try:
                            due_date_obj = datetime.strptime(args["due_date"], "%Y-%m-%d")
                        except:
                            pass
                    
                    new_task = Task(
                        title=args.get("title"),
                        description=args.get("description", ""),
                        user_id=user_id,
                        status="todo",
                        due_date=due_date_obj,
                        priority=args.get("priority", "medium"),
                        category=args.get("category", "general")
                    )
                    db.add(new_task)
                    db.commit()
                    db.refresh(new_task)
                    
                    msg = f"✅ Created: {new_task.title}"
                    if new_task.priority != "medium":
                        msg += f" (Priority: {new_task.priority})"
                    if new_task.due_date:
                        msg += f" (Due: {new_task.due_date.strftime('%Y-%m-%d')})"
                    return msg

                elif fn_name == "list_tasks":
                    tasks = db.exec(select(Task).where(Task.user_id == user_id)).all()
                    if not tasks:
                        return "📋 No tasks found."
                    
                    task_list = []
                    for t in tasks:
                        status_icon = "✅" if t.status == "completed" else "⏳"
                        task_list.append(f"{status_icon} {t.title} (Priority: {t.priority})")
                    
                    return f"📋 Your tasks:\n" + "\n".join(task_list)

                elif fn_name == "delete_task":
                    keyword = args.get("keyword", "").lower()
                    tasks = db.exec(select(Task).where(Task.user_id == user_id)).all()
                    
                    for t in tasks:
                        if keyword in t.title.lower():
                            title = t.title
                            db.delete(t)
                            db.commit()
                            return f"🗑️ Deleted: {title}"
                    
                    return f"❌ Could not find a task matching '{keyword}'."

                elif fn_name == "complete_task":
                    keyword = args.get("keyword", "").lower()
                    tasks = db.exec(select(Task).where(Task.user_id == user_id)).all()
                    
                    for t in tasks:
                        if keyword in t.title.lower():
                            t.status = "completed"
                            db.commit()
                            return f"✅ Completed: {t.title}"
                    
                    return f"❌ Could not find a task matching '{keyword}'."

        # Normal reply if no tool needed
        return response_message.content or "Processed your request."

    except Exception as e:
        import traceback
        print("\n" + "="*60)
        print(f"❌ AGENT ERROR")
        print(f"User: {user_id}")
        print(f"Message: {message}")
        print(f"Error: {str(e)}")
        print("="*60)
        traceback.print_exc()
        print("="*60 + "\n")
        return f"⚠️ System Error: {str(e)}"
