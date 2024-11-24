"""Background tasks for model operations."""

from typing import Dict, Any, Optional, List
from celery import shared_task
from ..core.model_manager import model_manager
from ..core.celery_app import celery_app

@shared_task(bind=True, name="tasks.generate_response")
def generate_response(
    self,
    agent_id: int,
    message: str,
    context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Generate model response in background."""
    try:
        response = model_manager.generate_response(agent_id, message, context)
        return {
            "success": True,
            "response": response
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@shared_task(bind=True, name="tasks.batch_process")
def batch_process(
    self,
    agent_id: int,
    messages: List[str],
    context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Process multiple messages in background."""
    results = []
    for message in messages:
        try:
            response = model_manager.generate_response(agent_id, message, context)
            results.append({
                "success": True,
                "message": message,
                "response": response
            })
        except Exception as e:
            results.append({
                "success": False,
                "message": message,
                "error": str(e)
            })
    return {"results": results} 