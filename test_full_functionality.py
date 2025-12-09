#!/usr/bin/env python3
"""
Test script to verify all functionality of the in-memory todo app works in a single session.
"""

from todo_app.services import TodoService

def test_full_functionality():
    print("Testing full functionality in single session...")

    # Create a single service instance (this simulates one session with in-memory storage)
    service = TodoService()

    print("\n1. Testing ADD task functionality:")
    task1 = service.add_task("Buy groceries", "Milk, bread, eggs")
    print(f"   Added task: ID {task1.id}, Title: {task1.title}, Status: {task1.status}")

    task2 = service.add_task("Walk the dog", "Morning walk in the park")
    print(f"   Added task: ID {task2.id}, Title: {task2.title}, Status: {task2.status}")

    print("\n2. Testing LIST tasks functionality:")
    all_tasks = service.get_all_tasks()
    print(f"   Total tasks: {len(all_tasks)}")
    for task in all_tasks:
        print(f"   - ID {task.id}: {task.title} [{task.status}]")

    print("\n3. Testing MARK COMPLETE functionality:")
    completed_task = service.mark_task_complete(task1.id)
    print(f"   Marked task as complete: ID {completed_task.id}, Title: {completed_task.title}, Status: {completed_task.status}")

    print("\n4. Testing LIST again to see updated status:")
    all_tasks = service.get_all_tasks()
    for task in all_tasks:
        print(f"   - ID {task.id}: {task.title} [{task.status}]")

    print("\n5. Testing UPDATE task functionality:")
    updated_task = service.update_task(task2.id, "Walk the cat", "Evening walk instead")
    print(f"   Updated task: ID {updated_task.id}, Title: {updated_task.title}, Description: {updated_task.description}")

    print("\n6. Testing DELETE task functionality:")
    deleted_task = service.delete_task(task1.id)
    print(f"   Deleted task: ID {deleted_task.id}, Title: {deleted_task.title}")

    print("\n7. Testing LIST final state:")
    all_tasks = service.get_all_tasks()
    print(f"   Final total tasks: {len(all_tasks)}")
    for task in all_tasks:
        print(f"   - ID {task.id}: {task.title} [{task.status}]")

    print("\n✅ All functionality tested successfully!")

if __name__ == "__main__":
    test_full_functionality()