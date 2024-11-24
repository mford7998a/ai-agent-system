"""Background tasks for chat operations."""

from typing import Dict, Any, List, Optional
from celery import shared_task
from ..core.group_chat import GroupChatOrchestrator
from ..core.celery_app import celery_app
from ..db.session import SessionLocal

@shared_task(bind=True, name="tasks.process_group_message")
def process_group_message(
    self,
    chat_id: int,
    message: str,
    sender_id: Optional[int] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Process group chat message in background."""
    db = SessionLocal()
    try:
        orchestrator = GroupChatOrchestrator(db)
        responses = orchestrator.process_message(
            session_id=chat_id,
            content=message,
            sender_id=sender_id,
            metadata=metadata
        )
        return {
            "success": True,
            "responses": responses
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
    finally:
        db.close()

@shared_task(bind=True, name="tasks.batch_process_messages")
def batch_process_messages(
    self,
    chat_id: int,
    messages: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Process multiple messages in background."""
    db = SessionLocal()
    try:
        orchestrator = GroupChatOrchestrator(db)
        results = []
        for msg in messages:
            try:
                responses = orchestrator.process_message(
                    session_id=chat_id,
                    content=msg["content"],
                    sender_id=msg.get("sender_id"),
                    metadata=msg.get("metadata")
                )
                results.append({
                    "success": True,
                    "message": msg,
                    "responses": responses
                })
            except Exception as e:
                results.append({
                    "success": False,
                    "message": msg,
                    "error": str(e)
                })
        return {"results": results}
    finally:
        db.close() 