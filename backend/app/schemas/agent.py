from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Optional
from datetime import datetime
import re

class ToolAssignment(BaseModel):
    tool_id: int = Field(..., gt=0)
    config: Optional[Dict[str, Any]] = Field(default_factory=dict)

    @validator('config')
    def validate_config(cls, v: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(v, dict):
            raise ValueError('Config must be a dictionary')
        return v

class AgentBase(BaseModel):
    """Base schema for Agent."""
    name: str
    description: Optional[str] = None
    role: str
    system_prompt: str
    model_config: Dict
    tools: List[int] = []
    is_system: bool = False
    metadata: Dict = {}

class AgentCreate(AgentBase):
    """Schema for creating an Agent."""
    pass

class AgentUpdate(BaseModel):
    """Schema for updating an Agent."""
    name: Optional[str] = None
    description: Optional[str] = None
    role: Optional[str] = None
    system_prompt: Optional[str] = None
    model_config: Optional[Dict] = None
    tools: Optional[List[int]] = None
    metadata: Optional[Dict] = None

class AgentResponse(AgentBase):
    """Schema for Agent response."""
    id: int
    status: str = "active"

    class Config:
        """Pydantic config."""
        from_attributes = True