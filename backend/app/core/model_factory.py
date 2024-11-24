from typing import Dict, Any
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

class ModelFactory:
    @staticmethod
    def create_model(provider: str, config: Dict[str, Any]) -> BaseChatModel:
        if provider.lower() == "openai":
            return ChatOpenAI(
                model_name=config.get("model_name", "gpt-4"),
                temperature=config.get("temperature", 0.7),
                api_key=config.get("api_key")
            )
        elif provider.lower() == "anthropic":
            return ChatAnthropic(
                model=config.get("model_name", "claude-3-opus"),
                temperature=config.get("temperature", 0.7),
                api_key=config.get("api_key")
            )
        elif provider.lower() == "google":
            return ChatGoogleGenerativeAI(
                model=config.get("model_name", "gemini-pro"),
                temperature=config.get("temperature", 0.7),
                api_key=config.get("api_key")
            )
        elif provider.lower() == "groq":
            return ChatGroq(
                model_name=config.get("model_name", "mixtral-8x7b-32768"),
                temperature=config.get("temperature", 0.7),
                api_key=config.get("api_key"),
                base_url=config.get("base_url", "https://api.groq.com/v1")
            )
        else:
            raise ValueError(f"Unsupported model provider: {provider}") 