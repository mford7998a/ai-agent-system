"""Background tasks for code operations."""

from typing import Dict, Any, Optional, List
from celery import shared_task
from ..core.execution_engine import ExecutionEngine
from ..core.celery_app import celery_app

execution_engine = ExecutionEngine()

@shared_task(bind=True, name="tasks.execute_code")
def execute_code(
    self,
    code: str,
    language: str,
    env_vars: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """Execute code in background."""
    try:
        result = execution_engine.execute_code(code, language, env_vars)
        return result
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "output": None
        }

@shared_task(bind=True, name="tasks.batch_execute")
def batch_execute(
    self,
    code_blocks: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Execute multiple code blocks in background."""
    results = []
    for block in code_blocks:
        try:
            result = execution_engine.execute_code(
                code=block["code"],
                language=block["language"],
                env_vars=block.get("env_vars")
            )
            results.append({
                "success": True,
                "block": block,
                "result": result
            })
        except Exception as e:
            results.append({
                "success": False,
                "block": block,
                "error": str(e)
            })
    return {"results": results} 