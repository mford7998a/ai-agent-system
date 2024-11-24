"""Tool schemas."""

from typing import Dict, Optional
from pydantic import BaseModel

class ToolBase(BaseModel):
    """Base schema for Tool."""
    name: str
    description: str
    is_system: bool = False
    is_available: bool = True
    config_schema: Optional[Dict] = None

class ToolCreate(ToolBase):
    """Schema for creating a Tool."""
    pass

class ToolUpdate(BaseModel):
    """Schema for updating a Tool."""
    name: Optional[str] = None
    description: Optional[str] = None
    is_available: Optional[bool] = None
    config_schema: Optional[Dict] = None

class ToolResponse(ToolBase):
    """Schema for Tool response."""
    id: int

    class Config:
        """Pydantic config."""
        from_attributes = True 