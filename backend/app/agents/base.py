from typing import Dict, Any, List
from abc import ABC, abstractmethod
from ..tools.base import BaseTool

class BaseAgent(ABC):
    def __init__(
        self,
        name: str,
        role: str,
        description: str,
        model_config: Dict[str, Any],
        tools: List[BaseTool] = None
    ):
        self.name = name
        self.role = role
        self.description = description
        self.model_config = model_config
        self.tools = tools or []
        self.context = {}
        
    def add_tool(self, tool: BaseTool):
        self.tools.append(tool)
        
    def remove_tool(self, tool_name: str):
        self.tools = [t for t in self.tools if t.name != tool_name]
        
    def set_context(self, context: Dict[str, Any]):
        self.context.update(context)
        
    @abstractmethod
    async def process_message(self, message: str) -> str:
        pass
        
    @abstractmethod
    async def execute_tool(self, tool_name: str, **kwargs) -> Any:
        pass