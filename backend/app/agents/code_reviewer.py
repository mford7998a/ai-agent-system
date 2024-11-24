from typing import Dict, Any
from .base import BaseAgent
from langchain.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

class CodeReviewerAgent(BaseAgent):
    def __init__(self, name: str, model_config: Dict[str, Any], **kwargs):
        super().__init__(
            name=name,
            role="code_reviewer",
            description="Specialized agent for reviewing and analyzing code",
            model_config=model_config,
            **kwargs
        )
        self.llm = ChatOpenAI(
            model_name=model_config.get("model_name", "gpt-4"),
            temperature=model_config.get("temperature", 0.3),
            api_key=model_config.get("api_key")
        )
        
    async def process_message(self, message: str) -> str:
        messages = [
            SystemMessage(content=f"""You are a code review agent named {self.name}.
            Your task is to review code for best practices, bugs, and improvements.
            Current context: {self.context}"""),
            HumanMessage(content=message)
        ]
        
        response = await self.llm.agenerate([messages])
        return response.generations[0][0].text
        
    async def execute_tool(self, tool_name: str, **kwargs) -> Any:
        tool = next((t for t in self.tools if t.name == tool_name), None)
        if not tool:
            raise ValueError(f"Tool {tool_name} not found")
        
        return await tool.execute(**kwargs) 