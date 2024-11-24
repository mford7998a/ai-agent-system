"""Group chat management endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...core.group_chat import GroupChatOrchestrator
from ...db.session import get_db
from ...schemas.chat import (
    GroupChatCreate,
    GroupChatResponse,
    GroupChatUpdate,
    ChatMessageResponse
)

router = APIRouter()

@router.post("/", response_model=GroupChatResponse)
async def create_group_chat(
    chat_data: GroupChatCreate,
    db: Session = Depends(get_db)
) -> GroupChatResponse:
    """Create a new group chat."""
    orchestrator = GroupChatOrchestrator(db)
    try:
        chat = await orchestrator.create_chat(
            name=chat_data.name,
            agents=chat_data.agent_ids,
            config=chat_data.config
        )
        return chat
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{chat_id}/message")
async def send_message(
    chat_id: int,
    content: str,
    db: Session = Depends(get_db)
) -> List[ChatMessageResponse]:
    """Send a message to the group chat."""
    orchestrator = GroupChatOrchestrator(db)
    try:
        responses = await orchestrator.process_message(
            session_id=chat_id,
            content=content
        )
        return responses
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{chat_id}/history")
async def get_chat_history(
    chat_id: int,
    limit: int = None,
    db: Session = Depends(get_db)
) -> List[ChatMessageResponse]:
    """Get chat history."""
    orchestrator = GroupChatOrchestrator(db)
    try:
        return await orchestrator.get_chat_history(chat_id, limit)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{chat_id}")
async def update_group_chat(
    chat_id: int,
    chat_data: GroupChatUpdate,
    db: Session = Depends(get_db)
) -> GroupChatResponse:
    """Update group chat settings."""
    orchestrator = GroupChatOrchestrator(db)
    try:
        # Implementation needed
        raise NotImplementedError("Update functionality not implemented yet")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{chat_id}")
async def end_group_chat(chat_id: int, db: Session = Depends(get_db)):
    """End a group chat session."""
    orchestrator = GroupChatOrchestrator(db)
    try:
        await orchestrator.end_chat(chat_id)
        return {"status": "success", "message": "Chat ended"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) 