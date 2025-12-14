#!/usr/bin/env python3
"""
Demo script showing how the CLI app works in a single session
"""

from todo_app.services import TodoService

def demo():
    print("🎯 CLI App Demo - Single Session")
    print("=" * 40)

    # Create service instance (this represents one session of in-memory storage)
    service = TodoService()

    print("\n1. Adding tasks...")
    task1 = service.add_task("Burger", "Make burger for dinner")
    print(f"   ✓ Added: {task1.title}")

    task2 = service.add_task("Pizza", "Order pizza for lunch")
    print(f"   ✓ Added: {task2.title}")

    print("\n2. Listing all tasks...")
    tasks = service.get_all_tasks()
    for task in tasks:
        status = "✓" if task.status == "completed" else "○"
        print(f"   {status} ID {task.id}: {task.title} - {task.description} [{task.status}]")

    print("\n3. Marking first task as complete...")
    completed_task = service.mark_task_complete(task1.id)
    print(f"   ✓ Marked as complete: {completed_task.title}")

    print("\n4. Listing tasks after completion...")
    tasks = service.get_all_tasks()
    for task in tasks:
        status = "✓" if task.status == "completed" else "○"
        print(f"   {status} ID {task.id}: {task.title} - {task.description} [{task.status}]")

    print("\n5. Updating a task...")
    updated_task = service.update_task(task2.id, "Calzone", "Order calzone instead")
    print(f"   ✓ Updated: {updated_task.title} - {updated_task.description}")

    print("\n6. Final list...")
    tasks = service.get_all_tasks()
    for task in tasks:
        status = "✓" if task.status == "completed" else "○"
        print(f"   {status} ID {task.id}: {task.title} - {task.description} [{task.status}]")

    print("\n7. Deleting a task...")
    deleted_task = service.delete_task(task1.id)
    print(f"   ✓ Deleted: {deleted_task.title}")

    print("\n8. Final list after deletion...")
    tasks = service.get_all_tasks()
    if not tasks:
        print("   No tasks remaining")
    else:
        for task in tasks:
            status = "✓" if task.status == "completed" else "○"
            print(f"   {status} ID {task.id}: {task.title} - {task.description} [{task.status}]")

    print("\n✅ Demo completed! All functionality works within a single session.")

if __name__ == "__main__":
    demo()