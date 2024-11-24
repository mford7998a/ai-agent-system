from typing import Dict, Any, List
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from .base import BaseAgent

class CodeWriterAgent(BaseAgent):
    def __init__(self, name: str, model_config: Dict[str, Any], **kwargs):
        super().__init__(
            name=name,
            role="code_writer",
            description="Specialized agent for writing and modifying code",
            model_config=model_config,
            **kwargs
        )
        self.llm = ChatOpenAI(
            model_name=model_config.get("model_name", "gpt-4"),
            temperature=model_config.get("temperature", 0.7),
            api_key=model_config.get("api_key")
        )
        self.conversation_history: List[Dict[str, str]] = []
        
    async def process_message(self, message: str) -> str:
        # Add file context if available
        context_prompt = ""
        if self.context.get("files"):
            context_prompt = "Available file context:\n"
            for file in self.context["files"]:
                context_prompt += f"\nFile: {file['name']}\nContent:\n{file['content']}\n"
        
        messages = [
            SystemMessage(content=f"""You are a code writer agent named {self.name}.
            Your task is to write and modify code based on requirements.
            {context_prompt}"""),
            *[AIMessage(content=m["content"]) if m["role"] == "assistant" 
              else HumanMessage(content=m["content"]) 
              for m in self.conversation_history],
            HumanMessage(content=message)
        ]
        
        response = await self.llm.agenerate([messages])
        response_text = response.generations[0][0].text
        
        # Update conversation history
        self.conversation_history.append({"role": "user", "content": message})
        self.conversation_history.append({"role": "assistant", "content": response_text})
        
        return response_text
        
    async def execute_tool(self, tool_name: str, **kwargs) -> Any:
        tool = next((t for t in self.tools if t.name == tool_name), None)
        if not tool:
            raise ValueError(f"Tool {tool_name} not found")
            
        result = await tool.execute(**kwargs)
        
        # Add tool execution result to conversation history
        self.conversation_history.append({
            "role": "system",
            "content": f"Tool execution result: {result}"
        })
        
        return result 