#!/usr/bin/env python3

import argparse
import sys
import os

# Add the project root directory to the path so we can import modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from todo_app.services import TodoService


def format_task_output(task):
    """Format a single task for display."""
    status_icon = "✓" if task.status == "completed" else "○"

    # Build the display string with priority and due date if available
    priority_part = f"[{task.priority}]"
    due_date_part = f" (Due: {task.due_date})" if task.due_date else ""

    return f"ID: {task.id} | {status_icon} {priority_part} {task.title}{due_date_part} - {task.description} [{task.status}]"


def interactive_mode(service):
    """Run the interactive mode for the CLI app."""
    print("🎯 Welcome to the Interactive Todo CLI App!")
    print("=" * 50)

    while True:
        print("\n📋 Main Menu:")
        print("1. Add a new task")
        print("2. List all tasks")
        print("3. Update a task")
        print("4. Mark a task as complete")
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

            # Get priority
            priority = input("Enter Priority (Low/Medium/High): ").strip().title()
            if priority not in ["Low", "Medium", "High"]:
                priority = "Medium"  # Default to Medium if invalid input
                print("⚠️  Invalid priority, defaulting to Medium")

            # Get due date
            due_date = input("Enter Due Date (YYYY-MM-DD) or press Enter to skip: ").strip()
            if due_date == "":
                due_date = None

            try:
                task = service.add_task(title, description, priority, due_date)
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

                print(f"Current priority: {task_to_update.priority}")
                new_priority = input("Enter new priority (Low/Medium/High) or press Enter to keep current: ").strip().title()
                if new_priority == "":
                    new_priority = None  # Keep current priority
                elif new_priority not in ["Low", "Medium", "High"]:
                    print("⚠️  Invalid priority, keeping current value")
                    new_priority = None

                print(f"Current due date: {task_to_update.due_date or 'None'}")
                new_due_date = input("Enter new due date (YYYY-MM-DD) or press Enter to keep current: ").strip()
                if new_due_date == "":
                    new_due_date = None  # Keep current due date
                elif new_due_date.lower() == "none" or new_due_date.lower() == "null":
                    new_due_date = None  # Allow user to clear due date

                updated_task = service.update_task(task_id, new_title, new_description, new_priority, new_due_date)
                print(f"✅ Task updated successfully: ID {updated_task.id}, Title: {updated_task.title}")
            except ValueError as e:
                print(f"❌ Error: {e}")
            except Exception:
                print("❌ Invalid input. Please enter valid numbers.")

        elif choice == "4":
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

                # Find the task to show details
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


def main():
    service = TodoService()

    parser = argparse.ArgumentParser(
        description="Todo CLI Application - Manage your tasks from the command line",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Add a task:           python cli.py add --title "Buy groceries" --description "Milk, bread, eggs"
  List all tasks:       python cli.py list
  Mark as complete:     python cli.py complete --id 1
  Update a task:        python cli.py update --id 1 --title "Updated title"
  Delete a task:        python cli.py delete --id 1
        """.strip()
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add Task Command
    add_parser = subparsers.add_parser("add", help="Add a new todo task")
    add_parser.add_argument("--title", required=True, help="Title of the task")
    add_parser.add_argument("--description", default="", help="Description of the task")
    add_parser.add_argument("--priority", default="Medium", choices=["Low", "Medium", "High"], help="Priority of the task (Low/Medium/High)")
    add_parser.add_argument("--due-date", default=None, help="Due date of the task (YYYY-MM-DD)")

    # List Tasks Command
    list_parser = subparsers.add_parser("list", help="List all todo tasks")

    # Complete Task Command
    complete_parser = subparsers.add_parser("complete", help="Mark a task as complete")
    complete_parser.add_argument("--id", type=int, required=True, help="ID of the task to complete")

    # Update Task Command
    update_parser = subparsers.add_parser("update", help="Update an existing task")
    update_parser.add_argument("--id", type=int, required=True, help="ID of the task to update")
    update_parser.add_argument("--title", required=False, help="New title for the task")
    update_parser.add_argument("--description", required=False, help="New description for the task")
    update_parser.add_argument("--priority", required=False, choices=["Low", "Medium", "High"], help="New priority for the task (Low/Medium/High)")
    update_parser.add_argument("--due-date", required=False, help="New due date for the task (YYYY-MM-DD)")

    # Delete Task Command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("--id", type=int, required=True, help="ID of the task to delete")

    # Check if no arguments were provided (interactive mode)
    if len(sys.argv) == 1:
        interactive_mode(service)
        return

    args = parser.parse_args()

    try:
        if args.command == "add":
            task = service.add_task(args.title, args.description, args.priority, args.due_date)
            print(f"✓ Task added successfully: ID {task.id}, Title: {task.title}")
        elif args.command == "list":
            tasks = service.get_all_tasks()
            if not tasks:
                print("ℹ️  No tasks found.")
            else:
                print("📋 All Tasks:")
                for task in tasks:
                    print(f"  {format_task_output(task)}")
        elif args.command == "complete":
            completed_task = service.mark_task_complete(args.id)
            print(f"✓ Task marked as complete: ID {completed_task.id}, Title: {completed_task.title}")
        elif args.command == "update":
            updated_task = service.update_task(args.id, args.title, args.description, args.priority, args.due_date)
            print(f"✓ Task updated successfully: ID {updated_task.id}, Title: {updated_task.title}")
        elif args.command == "delete":
            deleted_task = service.delete_task(args.id)
            print(f"✓ Task deleted successfully: ID {deleted_task.id}, Title: {deleted_task.title}")
        else:
            # This should not happen if argparse is working correctly
            parser.print_help()
            sys.exit(1)
    except ValueError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
