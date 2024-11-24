from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class CustomAgentBase(BaseModel):
    name: str
    description: Optional[str] = None
    system_prompt: str
    model_provider_id: int
    model_name: str
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)
    tools: List[int] = []
    metadata: Dict = {}

class CustomAgentCreate(CustomAgentBase):
    pass

class CustomAgentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    system_prompt: Optional[str] = None
    model_name: Optional[str] = None
    temperature: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    tools: Optional[List[int]] = None
    metadata: Optional[Dict] = None

class CustomAgentResponse(CustomAgentBase):
    id: int

    class Config:
        from_attributes = True