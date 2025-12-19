from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
from datetime import datetime, timedelta
from typing import Optional
import re

router = APIRouter(prefix="/api/ai", tags=["ai"])


class TaskParseRequest(BaseModel):
    input_text: str


@router.post("/parse-task")
async def parse_task(request: TaskParseRequest):
    """
    Parse natural language task input using intelligent rule-based parsing.
    No API keys required!
    
    Example: "Buy groceries tomorrow at 5pm" 
    Returns: {title, due_date, priority, category, tags}
    """
    
    input_text = request.input_text.strip()
    
    # Initialize parsed data
    parsed_data = {
        "title": input_text,
        "due_date": None,
        "priority": "medium",
        "category": "Personal",
        "tags": ""
    }
    
    lower_input = input_text.lower()
    
    # Extract priority from keywords
    if any(word in lower_input for word in ["urgent", "asap", "critical", "important", "high priority"]):
        parsed_data["priority"] = "high"
    elif any(word in lower_input for word in ["someday", "maybe", "later", "low priority"]):
        parsed_data["priority"] = "low"
    
    # Extract category from keywords
    if any(word in lower_input for word in ["work", "meeting", "project", "deadline", "office"]):
        parsed_data["category"] = "Work"
    elif any(word in lower_input for word in ["learn", "study", "course", "tutorial", "practice"]):
        parsed_data["category"] = "Learning"
    elif any(word in lower_input for word in ["buy", "shop", "groceries", "call", "personal", "home"]):
        parsed_data["category"] = "Personal"
    
    # Extract date keywords
    now = datetime.now()
    
    if "tomorrow" in lower_input:
        tomorrow = now + timedelta(days=1)
        # Extract time if mentioned
        if " at " in lower_input:
            time_part = lower_input.split(" at ")[-1].strip()
            hour = extract_hour(time_part)
            if hour is not None:
                parsed_data["due_date"] = tomorrow.replace(hour=hour, minute=0, second=0).isoformat()
            else:
                parsed_data["due_date"] = tomorrow.replace(hour=23, minute=59).isoformat()
        else:
            parsed_data["due_date"] = tomorrow.replace(hour=23, minute=59).isoformat()
    
    elif "today" in lower_input:
        parsed_data["due_date"] = now.replace(hour=23, minute=59, second=0).isoformat()
    
    elif "tonight" in lower_input:
        parsed_data["due_date"] = now.replace(hour=20, minute=0, second=0).isoformat()
    
    elif "next week" in lower_input:
        next_week = now + timedelta(days=7)
        parsed_data["due_date"] = next_week.replace(hour=23, minute=59).isoformat()
    
    elif "friday" in lower_input or "monday" in lower_input or "tuesday" in lower_input:
        # Simple day-of-week parsing
        days_ahead = 1  # Default
        if "friday" in lower_input:
            days_ahead = (4 - now.weekday()) % 7 or 7
        elif "monday" in lower_input:
            days_ahead = (0 - now.weekday()) % 7 or 7
        
        target_date = now + timedelta(days=days_ahead)
        
        if " at " in lower_input:
            time_part = lower_input.split(" at ")[-1].strip()
            hour = extract_hour(time_part)
            if hour is not None:
                parsed_data["due_date"] = target_date.replace(hour=hour, minute=0, second=0).isoformat()
            else:
                parsed_data["due_date"] = target_date.replace(hour=23, minute=59).isoformat()
        else:
            parsed_data["due_date"] = target_date.replace(hour=23, minute=59).isoformat()
    
    # Clean up title - remove date/time keywords
    title = input_text
    keywords_to_remove = [
        "tomorrow", "today", "tonight", "next week", "friday", "monday", "tuesday",
        "urgent:", "asap:", "important:", " at ", "by "
    ]
    
    for keyword in keywords_to_remove:
        title = title.replace(keyword, "").replace(keyword.capitalize(), "")
    
    # Remove time patterns (e.g., "5pm", "17:00")
    title = re.sub(r'\d{1,2}(:\d{2})?\s?(am|pm|AM|PM)?', '', title)
    
    # Clean up extra spaces
    title = ' '.join(title.split())
    
    parsed_data["title"] = title.strip() or input_text
    
    return {
        "success": True,
        "data": parsed_data
    }


def extract_hour(time_str: str) -> Optional[int]:
    """Extract hour from time string like '5pm', '17:00', '8 pm'"""
    time_str = time_str.lower().strip()
    
    # Handle "5pm", "5 pm" format
    if "pm" in time_str or "am" in time_str:
        is_pm = "pm" in time_str
        hour_str = time_str.replace("pm", "").replace("am", "").strip()
        
        try:
            hour = int(hour_str.split(":")[0])
            if is_pm and hour != 12:
                hour += 12
            elif not is_pm and hour == 12:
                hour = 0
            
            if 0 <= hour <= 23:
                return hour
        except:
            pass
    
    # Handle "17:00" format
    if ":" in time_str:
        try:
            hour = int(time_str.split(":")[0])
            if 0 <= hour <= 23:
                return hour
        except:
            pass
    
    return None


@router.post("/suggest-tasks")
async def suggest_tasks(task_title: str):
    """
    Suggest subtasks or related tasks based on a main task.
    """
    
    suggestions = []
    lower_title = task_title.lower()
    
    if "party" in lower_title or "event" in lower_title:
        suggestions = ["Create guest list", "Book venue", "Order food/catering", "Send invitations", "Plan activities"]
    elif "project" in lower_title or "report" in lower_title:
        suggestions = ["Research topic", "Create outline", "Draft content", "Review and edit", "Submit final version"]
    elif "learn" in lower_title or "study" in lower_title:
        suggestions = ["Find learning resources", "Set study schedule", "Practice exercises", "Take notes", "Review and test"]
    elif "buy" in lower_title or "shop" in lower_title:
        suggestions = ["Make shopping list", "Check prices online", "Visit store", "Compare options", "Make purchase"]
    else:
        suggestions = ["Break down into smaller tasks", "Set deadline", "Gather required resources", "Start working", "Review progress"]
    
    return {
        "success": True,
        "suggestions": suggestions
    }
