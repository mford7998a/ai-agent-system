from typing import Any, Dict, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from ..models.chat import ChatSession, ChatMessage
from ..models.agent import Agent
from .agent_manager import AgentManager

class GroupChatOrchestrator:
    """Orchestrator class for group chat operations."""

    def __init__(self, db: Session):
        """Initialize group chat orchestrator."""
        self.db = db
        self.agent_manager = AgentManager()
        self.active_chats: Dict[int, Dict[str, Any]] = {}

    async def create_chat(
        self,
        name: str,
        agents: List[Agent],
        config: Dict[str, Any]
    ) -> ChatSession:
        """Create a new group chat session."""
        try:
            # Create chat session
            session = ChatSession(
                name=name,
                metadata={"config": config}
            )
            self.db.add(session)
            
            # Add participants
            session.participants.extend(agents)
            
            self.db.commit()
            self.db.refresh(session)
            
            # Initialize chat state
            self.active_chats[session.id] = {
                "agents": {agent.id: agent for agent in agents},
                "config": config,
                "status": "active"
            }
            
            return session
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Failed to create group chat: {str(e)}")

    async def process_message(
        self,
        session_id: int,
        content: str,
        sender_id: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[ChatMessage]:
        """Process a message in the group chat."""
        chat_state = self.active_chats.get(session_id)
        if not chat_state or chat_state["status"] != "active":
            raise ValueError(f"Chat session {session_id} not found or inactive")

        try:
            # Create user message
            user_message = ChatMessage(
                session_id=session_id,
                content=content,
                message_type="user",
                metadata=metadata or {}
            )
            self.db.add(user_message)
            
            responses = []
            # Get responses from all agents
            for agent_id, agent in chat_state["agents"].items():
                if agent_id != sender_id:  # Don't let agent respond to itself
                    response = await self.agent_manager.process_message(
                        agent_id,
                        content,
                        context={
                            "session_id": session_id,
                            "chat_config": chat_state["config"]
                        }
                    )
                    
                    agent_message = ChatMessage(
                        session_id=session_id,
                        agent_id=agent_id,
                        content=response,
                        message_type="agent",
                        metadata={"role": agent.role}
                    )
                    self.db.add(agent_message)
                    responses.append(agent_message)
            
            self.db.commit()
            return responses
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Failed to process message: {str(e)}")

    async def end_chat(self, session_id: int) -> None:
        """End a group chat session."""
        chat_state = self.active_chats.get(session_id)
        if not chat_state:
            raise ValueError(f"Chat session {session_id} not found")

        try:
            # Update session status
            session = self.db.query(ChatSession).filter(
                ChatSession.id == session_id
            ).first()
            session.status = "completed"
            session.metadata["completed_at"] = datetime.utcnow().isoformat()
            
            # Update chat state
            chat_state["status"] = "completed"
            
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Failed to end chat: {str(e)}")

    async def get_chat_history(
        self,
        session_id: int,
        limit: Optional[int] = None
    ) -> List[ChatMessage]:
        """Get chat history for a session."""
        query = self.db.query(ChatMessage).filter(
            ChatMessage.session_id == session_id
        ).order_by(ChatMessage.created_at.desc())
        
        if limit:
            query = query.limit(limit)
            
        return query.all()