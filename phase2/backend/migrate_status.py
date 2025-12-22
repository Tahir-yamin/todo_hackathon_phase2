"""
Database migration script to update task status values.
Run this once to migrate from old status values to new ones.
"""

import asyncio
from sqlmodel import Session, select
from db import engine
from models import Task


async def migrate_task_status():
    """Migrate task status from old values (pending/completed) to new values (todo/in_progress/completed)"""
    
    with Session(engine) as session:
        # Get all tasks
        statement = select(Task)
        tasks = session.exec(statement).all()
        
        updated_count = 0
        
        for task in tasks:
            # Migrate old status values
            if task.status == 'pending':
                task.status = 'todo'
                updated_count += 1
            elif task.status == 'completed':
                # Keep as 'completed'
                pass
            
            # Ensure completed flag matches status
            if task.status == 'completed':
                task.completed = True
            else:
                task.completed = False
        
        # Commit changes
        session.commit()
        
        print(f"✅ Migration complete! Updated {updated_count} tasks.")
        print(f"   Total tasks: {len(tasks)}")


if __name__ == "__main__":
    print("Starting task status migration...")
    asyncio.run(migrate_task_status())
