    async def _delete_task(self, session: Session, args: dict, user_id: str) -> dict:
        """Delete a task"""
        try:
            task_id = args["task_id"]
            task = session.get(Task, task_id)
            
            if not task:
                return {"success": False, "error": f"Task with ID {task_id} not found"}
            
            if task.user_id != user_id:
                return {"success": False, "error": "Unauthorized: Task belongs to another user"}
            
            title = task.title
            session.delete(task)
            session.commit()
            
            print(f"✅ Deleted task: {title}")
            
            return {
                "success": True,
                "message": f"Successfully deleted task: '{title}'"
            }
        except Exception as e:
            session.rollback()
            raise
    
    async def _bulk_complete_tasks(self, session: Session, user_id: str) -> dict:
        """Mark all incomplete tasks as completed"""
        try:
            # Get all incomplete tasks for this user
            statement = select(Task).where(
                Task.user_id == user_id,
                Task.status != "completed"
            )
            tasks = session.exec(statement).all()
            
            # Mark each as completed
            for task in tasks:
                task.status = "completed"
                task.updated_at = datetime.utcnow()
                session.add(task)
            
            session.commit()
            
            print(f"✅ Bulk completed {len(tasks)} tasks for user {user_id}")
            
            return {
                "success": True,
                "count": len(tasks),
                "message": f"Successfully marked {len(tasks)} tasks as completed"
            }
        except Exception as e:
            session.rollback()
            raise


# Global MCP server instance
mcp = MCPServer()
