from sqlalchemy import Column, String, JSON, Integer, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from .base import TimeStampedBase

group_chat_agents = Table(
    'group_chat_agents',
    TimeStampedBase.metadata,
    Column('group_chat_id', Integer, ForeignKey('group_chats.id')),
    Column('agent_id', Integer, ForeignKey('custom_agents.id'))
)

class GroupChat(TimeStampedBase):
    __tablename__ = "group_chats"
    
    name = Column(String, index=True)
    description = Column(String)
    max_iterations = Column(Integer, default=10)
    system_prompt = Column(String)
    is_active = Column(Boolean, default=True)
    metadata = Column(JSON)
    
    agents = relationship("CustomAgent", secondary=group_chat_agents)
    messages = relationship("GroupChatMessage", back_populates="group_chat")

class GroupChatMessage(TimeStampedBase):
    __tablename__ = "group_chat_messages"
    
    group_chat_id = Column(Integer, ForeignKey("group_chats.id"))
    agent_id = Column(Integer, ForeignKey("custom_agents.id"), nullable=True)
    role = Column(String)  # 'system', 'agent', 'user'
    content = Column(String)
    metadata = Column(JSON)
    
    group_chat = relationship("GroupChat", back_populates="messages")
    agent = relationship("CustomAgent") 