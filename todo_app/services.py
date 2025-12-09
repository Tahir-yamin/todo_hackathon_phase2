from typing import List, Optional
from todo_app.models import Task

class TodoService:
    def __init__(self):
        self._tasks: List[Task] = []
        self._next_id = 1

    def _generate_id(self) -> int:
        task_id = self._next_id
        self._next_id += 1
        return task_id

    def add_task(self, title: str, description: str, priority: str = "Medium", due_date: str = None) -> Task:
        if not title:
            raise ValueError("Title cannot be empty")
        if priority not in ["Low", "Medium", "High"]:
            raise ValueError("Priority must be 'Low', 'Medium', or 'High'")
        task = Task(
            id=self._generate_id(),
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            status="pending"
        )
        self._tasks.append(task)
        return task

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks in the in-memory storage."""
        return self._tasks.copy()  # Return a copy to prevent external modification

    def mark_task_complete(self, task_id: int) -> Task:
        """Mark a task as complete by its ID."""
        for task in self._tasks:
            if task.id == task_id:
                task.status = "completed"
                return task

        raise ValueError(f"Task with ID {task_id} not found")

    def update_task(self, task_id: int, new_title: Optional[str] = None, new_description: Optional[str] = None,
                    new_priority: Optional[str] = None, new_due_date: Optional[str] = None) -> Task:
        """Update a task's title, description, priority, and/or due_date by its ID."""
        for task in self._tasks:
            if task.id == task_id:
                # Update title if provided
                if new_title is not None:
                    if not new_title:
                        raise ValueError("Title cannot be empty")
                    task.title = new_title

                # Update description if provided
                if new_description is not None:
                    task.description = new_description

                # Update priority if provided
                if new_priority is not None:
                    if new_priority not in ["Low", "Medium", "High"]:
                        raise ValueError("Priority must be 'Low', 'Medium', or 'High'")
                    task.priority = new_priority

                # Update due_date if provided
                if new_due_date is not None:
                    task.due_date = new_due_date

                return task

        raise ValueError(f"Task with ID {task_id} not found")

    def delete_task(self, task_id: int) -> Task:
        """Delete a task by its ID."""
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                deleted_task = self._tasks.pop(i)
                return deleted_task

        raise ValueError(f"Task with ID {task_id} not found")
