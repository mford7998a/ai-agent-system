from typing import Dict, Any
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from .base import BaseAgent

class CodeValidatorAgent(BaseAgent):
    def __init__(self, name: str, model_config: Dict[str, Any], **kwargs):
        super().__init__(
            name=name,
            role="code_validator",
            description="Specialized agent for validating code quality and execution results",
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
            SystemMessage(content=f"""You are a code validation agent named {self.name}.
            Your task is to analyze code quality, execution results, and provide improvement suggestions.
            Focus on:
            1. Code quality and best practices
            2. Potential bugs and security issues
            3. Performance optimization
            4. Error handling
            5. Documentation and readability
            
            Current context: {self.context}"""),
            HumanMessage(content=message)
        ]
        
        response = await self.llm.agenerate([messages])
        return response.generations[0][0].text
        
    async def validate_code(self, code: str, execution_result: Dict[str, Any] = None) -> Dict[str, Any]:
        validation_prompt = f"""Please analyze this code:        ```
        {code}        ```
        """
        
        if execution_result:
            validation_prompt += f"""
            Execution Result:            ```
            {execution_result}            ```
            """
            
        response = await self.process_message(validation_prompt)
        
        return {
            "success": True,
            "validation_result": response
        }
        
    async def execute_tool(self, tool_name: str, **kwargs) -> Any:
        tool = next((t for t in self.tools if t.name == tool_name), None)
        if not tool:
            raise ValueError(f"Tool {tool_name} not found")
            
        return await tool.execute(**kwargs)