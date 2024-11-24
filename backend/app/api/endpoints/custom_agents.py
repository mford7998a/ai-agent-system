from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from ...db.session import get_db
from ...models.custom_agent import CustomAgent
from ...models.model_provider import ModelProvider
from ...core.custom_agent import CustomAgent as CustomAgentRuntime
from ...schemas.custom_agent import (
    CustomAgentCreate,
    CustomAgentUpdate,
    CustomAgentResponse
)

router = APIRouter()

@router.post("/", response_model=CustomAgentResponse)
async def create_custom_agent(
    agent_data: CustomAgentCreate,
    db: Session = Depends(get_db)
):
    # Validate model provider
    provider = db.query(ModelProvider).filter(
        ModelProvider.id == agent_data.model_provider_id
    ).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Model provider not found")
    
    # Create agent
    agent = CustomAgent(**agent_data.dict())
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent

@router.get("/{agent_id}/activate")
async def activate_custom_agent(
    agent_id: int,
    db: Session = Depends(get_db)
):
    agent = db.query(CustomAgent).filter(CustomAgent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    runtime_agent = CustomAgentRuntime(
        name=agent.name,
        system_prompt=agent.system_prompt,
        model_provider=agent.model_provider.name,
        model_config={
            "model_name": agent.model_name,
            "temperature": agent.temperature,
            "api_key": agent.model_provider.api_key,
            "base_url": agent.model_provider.base_url
        },
        tools=[tool for tool in agent.tools]
    )
    
    return {"status": "success", "message": f"Agent {agent.name} activated"} 