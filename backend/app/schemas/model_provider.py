from pydantic import BaseModel, HttpUrl
from typing import Dict, Any, Optional, List

class ModelInfo(BaseModel):
    id: str
    name: str
    context_window: Optional[int] = None
    pricing: Optional[Dict[str, float]] = None
    max_tokens: Optional[int] = None

class ModelProviderBase(BaseModel):
    """Base schema for ModelProvider."""
    name: str
    api_key: str
    base_url: HttpUrl
    is_active: bool = True
    supported_models: List[Dict[str, str]]
    config: Dict = {}

class ModelProviderCreate(ModelProviderBase):
    """Schema for creating a ModelProvider."""
    pass

class ModelProviderUpdate(BaseModel):
    """Schema for updating a ModelProvider."""
    api_key: Optional[str] = None
    base_url: Optional[HttpUrl] = None
    is_active: Optional[bool] = None
    supported_models: Optional[List[Dict[str, str]]] = None
    config: Optional[Dict] = None

class ModelProviderResponse(BaseModel):
    """Schema for ModelProvider response."""
    id: int
    name: str
    base_url: HttpUrl
    is_active: bool
    supported_models: List[Dict[str, str]]
    config: Dict

    class Config:
        """Pydantic config."""
        from_attributes = True 