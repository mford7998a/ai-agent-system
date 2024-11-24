from typing import Dict, Any
from abc import ABC, abstractmethod

class BaseTool(ABC):
    def __init__(self, name: str, description: str, config: Dict[str, Any] = None):
        self.name = name
        self.description = description
        self.config = config or {}
    
    @abstractmethod
    async def execute(self, **kwargs) -> Any:
        pass
    
    def validate_args(self, **kwargs) -> bool:
        return True 