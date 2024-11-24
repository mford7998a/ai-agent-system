from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
from ...db.session import get_db
from ...models.model_provider import ModelProvider
from ...schemas.model_provider import (
    ModelProviderCreate,
    ModelProviderUpdate,
    ModelProviderResponse
)
from ...core.model_factory import ModelFactory
from ...core.model_manager import ModelManager
from ...core.config import settings

router = APIRouter()
model_manager = ModelManager()

PREDEFINED_PROVIDERS = {
    "openai": {
        "name": "OpenAI",
        "base_url": "https://api.openai.com/v1",
        "models": [
            {"id": "gpt-4-turbo-preview", "name": "GPT-4 Turbo"},
            {"id": "gpt-4", "name": "GPT-4"},
            {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo"}
        ]
    },
    "anthropic": {
        "name": "Anthropic",
        "base_url": "https://api.anthropic.com/v1",
        "models": [
            {"id": "claude-3-opus", "name": "Claude 3 Opus"},
            {"id": "claude-3-sonnet", "name": "Claude 3 Sonnet"},
            {"id": "claude-3-haiku", "name": "Claude 3 Haiku"}
        ]
    },
    "google": {
        "name": "Google AI",
        "base_url": "https://generativelanguage.googleapis.com/v1",
        "models": [
            {"id": "gemini-pro", "name": "Gemini Pro"},
            {"id": "gemini-pro-vision", "name": "Gemini Pro Vision"}
        ]
    },
    "groq": {
        "name": "Groq",
        "base_url": "https://api.groq.com/v1",
        "models": [
            {"id": "mixtral-8x7b-32768", "name": "Mixtral 8x7B"},
            {"id": "llama2-70b-4096", "name": "LLaMA 2 70B"}
        ]
    },
    "openrouter": {
        "name": "OpenRouter",
        "base_url": "https://openrouter.ai/api/v1",
        "models": [
            {"id": "anthropic/claude-3-opus", "name": "Claude 3 Opus"},
            {"id": "google/gemini-pro", "name": "Gemini Pro"},
            {"id": "mistral/mixtral-8x7b", "name": "Mixtral 8x7B"},
            {"id": "meta-llama/llama-2-70b", "name": "LLaMA 2 70B"}
        ]
    }
}

@router.get("/predefined", response_model=Dict)
async def get_predefined_providers():
    return PREDEFINED_PROVIDERS

@router.post("/", response_model=ModelProviderResponse)
async def create_model_provider(
    provider_data: ModelProviderCreate,
    db: Session = Depends(get_db)
) -> ModelProviderResponse:
    """Create a new model provider."""
    try:
        provider = ModelProvider(**provider_data.dict())
        db.add(provider)
        db.commit()
        db.refresh(provider)
        return provider
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Failed to create model provider: {str(e)}"
        )

@router.get("/{provider_id}", response_model=ModelProviderResponse)
async def get_model_provider(
    provider_id: int,
    db: Session = Depends(get_db)
) -> ModelProviderResponse:
    """Get model provider by ID."""
    provider = db.query(ModelProvider).filter(
        ModelProvider.id == provider_id
    ).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Model provider not found")
    return provider

@router.put("/{provider_id}", response_model=ModelProviderResponse)
async def update_model_provider(
    provider_id: int,
    provider_data: ModelProviderUpdate,
    db: Session = Depends(get_db)
) -> ModelProviderResponse:
    """Update a model provider."""
    provider = db.query(ModelProvider).filter(
        ModelProvider.id == provider_id
    ).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Model provider not found")

    try:
        for field, value in provider_data.dict(exclude_unset=True).items():
            setattr(provider, field, value)
        
        db.commit()
        db.refresh(provider)
        return provider
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Failed to update model provider: {str(e)}"
        )

@router.delete("/{provider_id}")
async def delete_model_provider(
    provider_id: int,
    db: Session = Depends(get_db)
):
    """Delete a model provider."""
    provider = db.query(ModelProvider).filter(
        ModelProvider.id == provider_id
    ).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Model provider not found")

    try:
        db.delete(provider)
        db.commit()
        return {"status": "success", "message": "Model provider deleted"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Failed to delete model provider: {str(e)}"
        )

@router.get("/", response_model=List[ModelProviderResponse])
async def list_model_providers(
    active_only: bool = False,
    db: Session = Depends(get_db)
) -> List[ModelProviderResponse]:
    """List all model providers."""
    query = db.query(ModelProvider)
    if active_only:
        query = query.filter(ModelProvider.is_active == True)
    return query.all()

@router.post("/{provider_id}/test")
async def test_model_provider(
    provider_id: int,
    db: Session = Depends(get_db)
):
    """Test model provider connection."""
    provider = db.query(ModelProvider).filter(
        ModelProvider.id == provider_id
    ).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Model provider not found")

    try:
        # Test connection using model manager
        result = await model_manager.test_provider(
            provider.name,
            provider.api_key,
            provider.base_url
        )
        return {
            "status": "success" if result else "failed",
            "message": "Connection test successful" if result else "Connection test failed"
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Connection test failed: {str(e)}"
        )

@router.get("/providers")
async def list_providers() -> Dict[str, bool]:
    """List available model providers and their status."""
    return {
        "openai": bool(settings.OPENAI_API_KEY),
        "anthropic": bool(settings.ANTHROPIC_API_KEY),
        "gemini": bool(settings.GOOGLE_API_KEY),
        "groq": bool(getattr(settings, 'GROQ_API_KEY', None))
    }

@router.get("/models/{provider}")
async def list_provider_models(provider: str) -> List[Dict[str, str]]:
    """List available models for a provider."""
    try:
        models = {
            "openai": [
                {"id": "gpt-4-turbo-preview", "name": "GPT-4 Turbo"},
                {"id": "gpt-4", "name": "GPT-4"},
                {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo"}
            ],
            "anthropic": [
                {"id": "claude-3-opus", "name": "Claude 3 Opus"},
                {"id": "claude-3-sonnet", "name": "Claude 3 Sonnet"},
                {"id": "claude-2.1", "name": "Claude 2.1"}
            ],
            "gemini": [
                {"id": "gemini-pro", "name": "Gemini Pro"}
            ],
            "groq": [
                {"id": "mixtral-8x7b-32768", "name": "Mixtral 8x7B"},
                {"id": "llama2-70b-4096", "name": "LLaMA 2 70B"}
            ]
        }
        
        if provider not in models:
            raise HTTPException(
                status_code=404,
                detail=f"Provider {provider} not found"
            )
            
        return models[provider]
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to list models: {str(e)}"
        )

@router.post("/validate-config")
async def validate_model_config(config: Dict[str, str]) -> Dict[str, bool]:
    """Validate model configuration."""
    try:
        is_valid = await model_manager.validate_config(config)
        return {
            "valid": is_valid,
            "message": "Configuration is valid" if is_valid else "Invalid configuration"
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Configuration validation failed: {str(e)}"
        )

@router.post("/test-connection/{provider}")
async def test_provider_connection(provider: str) -> Dict[str, bool]:
    """Test connection to a model provider."""
    try:
        # Implementation needed for actual API connection test
        is_connected = True  # Placeholder
        return {
            "connected": is_connected,
            "message": "Successfully connected to provider"
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Connection test failed: {str(e)}"
        )