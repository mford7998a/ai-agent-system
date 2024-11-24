from typing import Any, Dict, List, Optional
import asyncio
from ..core.model_manager import ModelManager
from ..core.tool_manager import ToolManager

class CustomAgent:
    """Runtime class for custom agents."""

    def __init__(
        self,
        name: str,
        system_prompt: str,
        model_provider: str,
        model_config: Dict[str, Any],
        tools: List[int]
    ):
        """Initialize custom agent."""
        self.name = name
        self.system_prompt = system_prompt
        self.model_provider = model_provider
        self.model_config = model_config
        self.tool_ids = tools
        self.model_manager = ModelManager()
        self.tool_manager = ToolManager()
        self.context: Dict[str, Any] = {}

    async def initialize(self):
        """Initialize agent resources."""
        # Load tools
        self.tools = []
        for tool_id in self.tool_ids:
            tool = await self.tool_manager.get_tool(tool_id)
            if tool and tool.is_available:
                self.tools.append(tool)

    async def process_message(
        self,
        message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Process a message using the agent's model and tools."""
        if context:
            self.context.update(context)

        try:
            # Generate response using model
            response = await self.model_manager.generate_response(
                self.name,
                message,
                {
                    "system_prompt": self.system_prompt,
                    "tools": [t.name for t in self.tools],
                    "context": self.context
                }
            )
            return response
        except Exception as e:
            raise ValueError(f"Failed to process message: {str(e)}")

    async def execute_tool(
        self,
        tool_name: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a tool with given parameters."""
        for tool in self.tools:
            if tool.name == tool_name:
                return await self.tool_manager.execute_tool(tool, params)
        raise ValueError(f"Tool {tool_name} not found or not available")

    async def cleanup(self):
        """Cleanup agent resources."""
        await self.model_manager.cleanup_model(self.name) 