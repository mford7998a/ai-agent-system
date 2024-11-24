"""Chat schemas."""

from typing import Dict, List, Optional
from pydantic import BaseModel

class ChatSessionBase(BaseModel):
    """Base schema for ChatSession."""
    name: str
    description: Optional[str] = None
    metadata: Dict = {}

class ChatSessionCreate(ChatSessionBase):
    """Schema for creating a ChatSession."""
    pass

class ChatSessionResponse(ChatSessionBase):
    """Schema for ChatSession response."""
    id: int
    status: str = "active"

    class Config:
        """Pydantic config."""
        from_attributes = True

class ChatMessageBase(BaseModel):
    """Base schema for ChatMessage."""
    content: str
    message_type: str
    agent_id: Optional[int] = None
    metadata: Dict = {}

class ChatMessageCreate(ChatMessageBase):
    """Schema for creating a ChatMessage."""
    pass

class ChatMessageResponse(ChatMessageBase):
    """Schema for ChatMessage response."""
    id: int
    session_id: int
    created_at: str

    class Config:
        """Pydantic config."""
        from_attributes = True

class GroupChatBase(BaseModel):
    """Base schema for GroupChat."""
    name: str
    config: Dict = {}
    agent_ids: List[int]

class GroupChatCreate(GroupChatBase):
    """Schema for creating a GroupChat."""
    pass

class GroupChatUpdate(BaseModel):
    """Schema for updating a GroupChat."""
    name: Optional[str] = None
    config: Optional[Dict] = None
    agent_ids: Optional[List[int]] = None

class GroupChatResponse(GroupChatBase):
    """Schema for GroupChat response."""
    id: int
    status: str = "active"

    class Config:
        """Pydantic config."""
        from_attributes = True

class GroupChatStatus(BaseModel):
    """Schema for GroupChat status response."""
    status: str
    message: str
    chat_id: int 