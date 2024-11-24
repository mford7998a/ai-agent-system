"""Model manager for handling different AI model providers."""

from typing import Any, Dict, List, Optional
import openai
import anthropic
from google.generativeai import GenerativeModel
import groq
from openai import OpenAI
from ..core.config import settings

class ModelManager:
    """Manager class for AI model operations."""

    def __init__(self):
        """Initialize model manager."""
        self.active_models: Dict[int, Dict[str, Any]] = {}
        self.setup_clients()

    def setup_clients(self):
        """Setup API clients for different providers."""
        self.clients = {
            "openai": OpenAI(api_key=settings.OPENAI_API_KEY),
            "anthropic": anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY) if settings.ANTHROPIC_API_KEY else None,
            "gemini": GenerativeModel('gemini-pro') if settings.GOOGLE_API_KEY else None,
            "groq": groq.Groq(api_key=settings.GROQ_API_KEY) if hasattr(settings, 'GROQ_API_KEY') else None
        }

    async def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate model configuration."""
        required_fields = ["provider", "model_name"]
        if not all(field in config for field in required_fields):
            return False

        provider = config["provider"]
        if provider not in self.clients or not self.clients[provider]:
            return False

        return True

    async def initialize_model(self, agent_id: int, config: Dict[str, Any]) -> None:
        """Initialize a model for an agent."""
        if not await self.validate_config(config):
            raise ValueError("Invalid model configuration")

        self.active_models[agent_id] = {
            "config": config,
            "provider": config["provider"],
            "model_name": config["model_name"],
            "context": []
        }

    async def generate_response(
        self,
        agent_id: int,
        message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate a response using the specified model."""
        model_info = self.active_models.get(agent_id)
        if not model_info:
            raise ValueError(f"No active model found for agent {agent_id}")

        provider = model_info["provider"]
        model_name = model_info["model_name"]
        
        try:
            if provider == "openai":
                response = await self._generate_openai(model_name, message, context)
            elif provider == "anthropic":
                response = await self._generate_anthropic(model_name, message, context)
            elif provider == "gemini":
                response = await self._generate_gemini(message, context)
            elif provider == "groq":
                response = await self._generate_groq(model_name, message, context)
            else:
                raise ValueError(f"Unsupported provider: {provider}")

            return response
        except Exception as e:
            raise ValueError(f"Failed to generate response: {str(e)}")

    async def _generate_openai(
        self,
        model: str,
        message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate response using OpenAI."""
        messages = []
        if context and "chat_history" in context:
            messages.extend(context["chat_history"])
        messages.append({"role": "user", "content": message})

        response = await self.clients["openai"].chat.completions.create(
            model=model,
            messages=messages
        )
        return response.choices[0].message.content

    async def _generate_anthropic(
        self,
        model: str,
        message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate response using Anthropic."""
        messages = []
        if context and "chat_history" in context:
            messages.extend(context["chat_history"])
        messages.append({"role": "user", "content": message})

        response = await self.clients["anthropic"].messages.create(
            model=model,
            messages=messages
        )
        return response.content[0].text

    async def _generate_gemini(
        self,
        message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate response using Google's Gemini."""
        response = await self.clients["gemini"].generate_content(message)
        return response.text

    async def _generate_groq(
        self,
        model: str,
        message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate response using Groq."""
        messages = []
        if context and "chat_history" in context:
            messages.extend(context["chat_history"])
        messages.append({"role": "user", "content": message})

        response = await self.clients["groq"].chat.completions.create(
            model=model,
            messages=messages
        )
        return response.choices[0].message.content

    async def cleanup_model(self, agent_id: int) -> None:
        """Cleanup model resources for an agent."""
        if agent_id in self.active_models:
            del self.active_models[agent_id] 