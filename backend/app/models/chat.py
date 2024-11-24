from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, JSON, Table
from sqlalchemy.orm import relationship

from ..db.base import Base

chat_participants = Table(
    'chat_participants',
    Base.metadata,
    Column('session_id', Integer, ForeignKey('chat_sessions.id')),
    Column('agent_id', Integer, ForeignKey('agents.id'))
)

class ChatSession(Base):
    """Chat session model."""
    
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    status = Column(String, default="active")
    metadata = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    messages = relationship("ChatMessage", back_populates="session")
    participants = relationship("Agent", secondary=chat_participants)

class ChatMessage(Base):
    """Chat message model."""
    
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"))
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=True)
    content = Column(String)
    message_type = Column(String)  # user, agent, system
    metadata = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("ChatSession", back_populates="messages")
    agent = relationship("Agent", back_populates="messages") 