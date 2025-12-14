from dataclasses import dataclass
from typing import Optional

@dataclass
class Task:
    id: int
    title: str
    description: str
    priority: str = "Medium"  # Options: 'Low', 'Medium', 'High'
    due_date: Optional[str] = None  # Format: 'YYYY-MM-DD'
    status: str = "pending"
