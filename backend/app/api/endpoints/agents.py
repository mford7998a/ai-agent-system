from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from ...db.session import get_db
from ...models.agent import Agent
from ...core.agent_manager import AgentManager
from ...schemas.agent import AgentCreate, AgentResponse, AgentUpdate

router = APIRouter()
agent_manager = AgentManager()

@router.post("/", response_model=AgentResponse)
async def create_agent(
    agent_data: AgentCreate,
    db: Session = Depends(get_db)
) -> AgentResponse:
    """Create a new agent."""
    try:
        agent = await agent_manager.create_agent(db, agent_data)
        return agent
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: int, db: Session = Depends(get_db)) -> AgentResponse:
    """Get agent by ID."""
    agent = await agent_manager.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@router.put("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: int,
    agent_data: AgentUpdate,
    db: Session = Depends(get_db)
) -> AgentResponse:
    """Update an agent."""
    try:
        agent = await agent_manager.update_agent(db, agent_id, agent_data)
        return agent
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{agent_id}")
async def delete_agent(agent_id: int, db: Session = Depends(get_db)):
    """Delete an agent."""
    try:
        await agent_manager.delete_agent(db, agent_id)
        return {"status": "success", "message": "Agent deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/", response_model=List[AgentResponse])
async def list_agents(
    status: str = None,
    db: Session = Depends(get_db)
) -> List[AgentResponse]:
    """List all agents."""
    return await agent_manager.list_agents(db, status)

@router.post("/{agent_id}/process")
async def process_message(
    agent_id: int,
    message: str,
    db: Session = Depends(get_db)
):
    """Process a message using an agent."""
    try:
        response = await agent_manager.process_message(agent_id, message)
        return {"response": response}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) 