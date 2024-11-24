from typing import Dict, Any, Set, Optional
from sqlalchemy import Column, String, JSON, ForeignKey, Table, Integer, Boolean, DateTime, select
from sqlalchemy.orm import relationship, Session
from sqlalchemy.sql import func
from .base import TimeStampedBase
from .tool import tool_configs
from datetime import datetime

class Agent(TimeStampedBase):
    """Agent model representing an AI agent in the system."""
    
    __tablename__ = "agents"

    # Required fields
    name: str = Column(String(100), index=True, nullable=False)
    role: str = Column(String(100), nullable=False)
    description: Optional[str] = Column(String(500), nullable=True)
    model_config: Dict[str, Any] = Column(JSON, default=dict, nullable=False)
    status: str = Column(
        String(20),
        default="inactive",
        nullable=False,
        server_default="inactive"
    )
    last_active: Optional[DateTime] = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        nullable=True
    )
    metadata: Dict[str, Any] = Column(
        JSON,
        default=dict,
        nullable=False,
        server_default="{}"
    )
    
    # Relationships with eager loading configuration
    tools = relationship(
        "Tool",
        secondary=tool_configs,
        back_populates="agents",
        lazy="joined",
        cascade="save-update, merge",
        collection_class=set
    )
    
    chat_messages = relationship(
        "ChatMessage",
        back_populates="agent",
        cascade="all, delete-orphan",
        lazy="dynamic",
        passive_deletes=True
    )
    
    group_chats = relationship(
        "GroupChat",
        secondary="group_chat_agents",
        back_populates="agents",
        lazy="joined",
        collection_class=set
    )

    def __init__(self, **kwargs: Any) -> None:
        """Initialize an Agent instance with provided kwargs."""
        super().__init__(**kwargs)
        self.model_config = kwargs.get('model_config', {})
        self.metadata = kwargs.get('metadata', {})

    @property
    def tool_configs(self) -> Dict[str, Any]:
        """Get tool configurations for this agent."""
        configs: Dict[str, Any] = {}
        
        if not hasattr(self, '_sa_instance_state') or not self._sa_instance_state.session:
            return configs
            
        session: Session = self._sa_instance_state.session
        
        for tool in self.tools:
            stmt = (
                select(tool_configs)
                .where(
                    tool_configs.c.agent_id == self.id,
                    tool_configs.c.tool_id == tool.id
                )
            )
            result = session.execute(stmt).first()
            configs[tool.name] = result.config if result else tool.default_config
            
        return configs

    @property
    def chat_count(self) -> int:
        """Get total number of unique chat sessions this agent participated in."""
        if self.chat_messages is None:
            return 0
        session_ids: Set[int] = {
            msg.session_id for msg in self.chat_messages if msg.session_id is not None
        }
        return len(session_ids)

    def can_use_tool(self, tool_name: str) -> bool:
        """Check if agent has access to a specific tool.
        
        Args:
            tool_name: The name of the tool to check.
            
        Returns:
            bool: True if the agent has access to the tool, False otherwise.
        """
        return any(t.name == tool_name for t in self.tools)

    def __repr__(self) -> str:
        """Return string representation of the Agent."""
        return f"<Agent(id={self.id}, name='{self.name}', role='{self.role}')>"