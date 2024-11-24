"""Task management endpoints."""

from typing import List
from fastapi import APIRouter, HTTPException
from app.core.task_monitor import TaskMonitor

router = APIRouter()

@router.get("/{task_id}")
async def get_task_status(task_id: str):
    """Get status of a task."""
    try:
        return await TaskMonitor.get_task_status(task_id)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to get task status: {str(e)}"
        )

@router.post("/batch-status")
async def get_tasks_status(task_ids: List[str]):
    """Get status of multiple tasks."""
    try:
        return await TaskMonitor.get_tasks_status(task_ids)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to get tasks status: {str(e)}"
        )

@router.delete("/{task_id}")
async def revoke_task(task_id: str, terminate: bool = False):
    """Revoke a running task."""
    try:
        result = await TaskMonitor.revoke_task(task_id, terminate)
        if not result["success"]:
            raise HTTPException(
                status_code=400,
                detail=result["error"]
            )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to revoke task: {str(e)}"
        )

@router.delete("/")
async def purge_tasks():
    """Purge all pending tasks."""
    try:
        result = await TaskMonitor.purge_tasks()
        if not result["success"]:
            raise HTTPException(
                status_code=400,
                detail=result["error"]
            )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to purge tasks: {str(e)}"
        ) 