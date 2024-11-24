"""File context schemas."""

from typing import Dict, Optional
from pydantic import BaseModel

class FileContextBase(BaseModel):
    """Base schema for FileContext."""
    name: str
    file_path: str
    content: str
    metadata: Dict = {}

class FileContextCreate(FileContextBase):
    """Schema for creating a FileContext."""
    pass

class FileContextUpdate(BaseModel):
    """Schema for updating a FileContext."""
    content: Optional[str] = None
    metadata: Optional[Dict] = None

class FileContextResponse(FileContextBase):
    """Schema for FileContext response."""
    id: int
    status: str = "active"

    class Config:
        """Pydantic config."""
        from_attributes = True 