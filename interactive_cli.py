#!/usr/bin/env python3
"""
Interactive Todo CLI Application
A user-friendly interface that prompts for input instead of requiring command-line arguments
"""

from todo_app.services import TodoService

def format_task_output(task):
    """Format a single task for display."""
    status_icon = "✓" if task.status == "completed" else "○"
    return f"ID: {task.id} | {status_icon} {task.title} - {task.description} [{task.status}]"

def main():
    service = TodoService()

    print("🎯 Welcome to the Interactive Todo CLI App!")
    print("=" * 50)

    while True:
        print("\n📋 Main Menu:")
        print("1. Add a new task")
        print("2. List all tasks")
        print("3. Mark a task as complete")
        print("4. Update a task")
        print("5. Delete a task")
        print("6. Exit")

        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == "1":
            # Add a new task
            print("\n📝 Adding a new task:")
            title = input("Enter task title: ").strip()
            if not title:
                print("❌ Title cannot be empty!")
                continue

            description = input("Enter task description (optional, press Enter to skip): ").strip()

            try:
                task = service.add_task(title, description)
                print(f"✅ Task added successfully! ID: {task.id}, Title: {task.title}")
            except ValueError as e:
                print(f"❌ Error: {e}")

        elif choice == "2":
            # List all tasks
            tasks = service.get_all_tasks()
            if not tasks:
                print("\nℹ️  No tasks found.")
            else:
                print(f"\n📋 All Tasks ({len(tasks)} total):")
                print("-" * 50)
                for task in tasks:
                    print(f"  {format_task_output(task)}")

        elif choice == "3":
            # Mark task as complete
            tasks = service.get_all_tasks()
            if not tasks:
                print("\nℹ️  No tasks found.")
                continue

            print("\n📋 Current Tasks:")
            for task in tasks:
                print(f"  {format_task_output(task)}")

            try:
                task_id = int(input("\nEnter task ID to mark as complete: ").strip())
                completed_task = service.mark_task_complete(task_id)
                print(f"✅ Task marked as complete: ID {completed_task.id}, Title: {completed_task.title}")
            except ValueError as e:
                print(f"❌ Error: {e}")
            except Exception:
                print("❌ Invalid task ID. Please enter a valid number.")

        elif choice == "4":
            # Update a task
            tasks = service.get_all_tasks()
            if not tasks:
                print("\nℹ️  No tasks found.")
                continue

            print("\n📋 Current Tasks:")
            for task in tasks:
                print(f"  {format_task_output(task)}")

            try:
                task_id = int(input("\nEnter task ID to update: ").strip())

                # Find the task to show current values
                task_to_update = None
                for task in tasks:
                    if task.id == task_id:
                        task_to_update = task
                        break

                if not task_to_update:
                    print("❌ Task not found with that ID.")
                    continue

                print(f"\nUpdating Task ID {task_id}:")
                print(f"Current title: {task_to_update.title}")
                new_title = input("Enter new title (or press Enter to keep current): ").strip()
                if new_title == "":
                    new_title = None  # Keep current title

                print(f"Current description: {task_to_update.description}")
                new_description = input("Enter new description (or press Enter to keep current): ").strip()
                if new_description == "":
                    new_description = None  # Keep current description

                updated_task = service.update_task(task_id, new_title, new_description)
                print(f"✅ Task updated successfully: ID {updated_task.id}, Title: {updated_task.title}")
            except ValueError as e:
                print(f"❌ Error: {e}")
            except Exception:
                print("❌ Invalid input. Please enter valid numbers.")

        elif choice == "5":
            # Delete a task
            tasks = service.get_all_tasks()
            if not tasks:
                print("\nℹ️  No tasks found.")
                continue

            print("\n📋 Current Tasks:")
            for task in tasks:
                print(f"  {format_task_output(task)}")

            try:
                task_id = int(input("\nEnter task ID to delete: ").strip())

                # Confirm deletion
                task_to_delete = None
                for task in tasks:
                    if task.id == task_id:
                        task_to_delete = task
                        break

                if not task_to_delete:
                    print("❌ Task not found with that ID.")
                    continue

                confirm = input(f"Are you sure you want to delete task '{task_to_delete.title}'? (y/N): ").strip().lower()
                if confirm in ['y', 'yes']:
                    deleted_task = service.delete_task(task_id)
                    print(f"✅ Task deleted successfully: ID {deleted_task.id}, Title: {deleted_task.title}")
                else:
                    print("❌ Deletion cancelled.")
            except ValueError as e:
                print(f"❌ Error: {e}")
            except Exception:
                print("❌ Invalid task ID. Please enter a valid number.")

        elif choice == "6":
            # Exit
            print("\n👋 Thank you for using the Todo CLI App! Goodbye!")
            break

        else:
            print("\n❌ Invalid choice. Please enter a number between 1-6.")

if __name__ == "__main__":
    main()