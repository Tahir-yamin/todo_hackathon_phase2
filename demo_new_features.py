#!/usr/bin/env python3
"""
Demo script showing the new intermediate features of the CLI app
"""

from todo_app.services import TodoService

def demo():
    print("🎯 CLI App Demo - New Intermediate Features")
    print("=" * 50)

    # Create service instance (this represents one session of in-memory storage)
    service = TodoService()

    print("\n1. Adding tasks with priority and due date...")
    task1 = service.add_task("Buy groceries", "Milk, bread, eggs", "High", "2024-12-31")
    print(f"   ✓ Added: {task1.title} [Priority: {task1.priority}, Due: {task1.due_date}]")

    task2 = service.add_task("Walk the dog", "Morning walk in the park", "Medium", "2024-12-30")
    print(f"   ✓ Added: {task2.title} [Priority: {task2.priority}, Due: {task2.due_date}]")

    task3 = service.add_task("Read a book", "Finish the novel", "Low")  # No due date
    print(f"   ✓ Added: {task3.title} [Priority: {task3.priority}, Due: {task3.due_date}]")

    print("\n2. Listing all tasks with new fields...")
    tasks = service.get_all_tasks()
    for task in tasks:
        status = "✓" if task.status == "completed" else "○"
        due_date_str = f" (Due: {task.due_date})" if task.due_date else ""
        print(f"   {status} ID {task.id}: [{task.priority}] {task.title}{due_date_str} - {task.description} [{task.status}]")

    print("\n3. Updating a task with new priority and due date...")
    updated_task = service.update_task(task2.id, new_priority="High", new_due_date="2024-12-29")
    print(f"   ✓ Updated: {updated_task.title} [Priority: {updated_task.priority}, Due: {updated_task.due_date}]")

    print("\n4. Final list after update...")
    tasks = service.get_all_tasks()
    for task in tasks:
        status = "✓" if task.status == "completed" else "○"
        due_date_str = f" (Due: {task.due_date})" if task.due_date else ""
        print(f"   {status} ID {task.id}: [{task.priority}] {task.title}{due_date_str} - {task.description} [{task.status}]")

    print("\n✅ Demo completed! All new features work correctly.")

if __name__ == "__main__":
    demo()