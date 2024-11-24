"""Task monitoring and result handling."""

from typing import Dict, Any, Optional, List
from celery.result import AsyncResult
from .celery_app import celery_app

class TaskMonitor:
    """Monitor and manage background tasks."""

    @staticmethod
    async def get_task_status(task_id: str) -> Dict[str, Any]:
        """Get status of a task by ID."""
        result = AsyncResult(task_id, app=celery_app)
        return {
            "task_id": task_id,
            "status": result.status,
            "result": result.result if result.ready() else None,
            "error": str(result.result) if result.failed() else None
        }

    @staticmethod
    async def get_tasks_status(task_ids: List[str]) -> List[Dict[str, Any]]:
        """Get status of multiple tasks."""
        return [
            await TaskMonitor.get_task_status(task_id)
            for task_id in task_ids
        ]

    @staticmethod
    async def revoke_task(task_id: str, terminate: bool = False) -> Dict[str, Any]:
        """Revoke a running task."""
        try:
            celery_app.control.revoke(task_id, terminate=terminate)
            return {
                "success": True,
                "message": f"Task {task_id} revoked"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    @staticmethod
    async def purge_tasks() -> Dict[str, Any]:
        """Purge all pending tasks."""
        try:
            celery_app.control.purge()
            return {
                "success": True,
                "message": "All pending tasks purged"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            } 