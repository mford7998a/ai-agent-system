from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

from ..models.agent import Agent
from ..schemas.agent import AgentCreate, AgentUpdate
from .model_manager import ModelManager

class AgentManager:
    """Manager class for AI agents."""

    def __init__(self):
        """Initialize agent manager."""
        self.active_agents: Dict[int, Any] = {}
        self.model_manager = ModelManager()

    async def create_agent(
        self,
        db: Session,
        agent_data: AgentCreate
    ) -> Agent:
        """Create a new agent."""
        try:
            # Validate model configuration
            if not await self.model_manager.validate_config(agent_data.model_config):
                raise ValueError("Invalid model configuration")

            # Create agent
            agent = Agent(**agent_data.dict())
            db.add(agent)
            db.commit()
            db.refresh(agent)

            # Initialize model
            await self.model_manager.initialize_model(
                agent.id,
                agent.model_config
            )

            return agent
        except Exception as e:
            db.rollback()
            raise ValueError(f"Failed to create agent: {str(e)}")

    async def get_agent(self, agent_id: int) -> Optional[Agent]:
        """Get an agent by ID."""
        return self.active_agents.get(agent_id)

    async def update_agent(
        self,
        db: Session,
        agent_id: int,
        agent_data: AgentUpdate
    ) -> Agent:
        """Update an agent."""
        agent = db.query(Agent).filter(Agent.id == agent_id).first()
        if not agent:
            raise ValueError(f"Agent {agent_id} not found")

        try:
            # Update model configuration if provided
            if agent_data.model_config:
                if not await self.model_manager.validate_config(agent_data.model_config):
                    raise ValueError("Invalid model configuration")
                await self.model_manager.update_model(
                    agent.id,
                    agent_data.model_config
                )

            # Update agent data
            for field, value in agent_data.dict(exclude_unset=True).items():
                setattr(agent, field, value)

            db.commit()
            db.refresh(agent)
            return agent
        except Exception as e:
            db.rollback()
            raise ValueError(f"Failed to update agent: {str(e)}")

    async def delete_agent(self, db: Session, agent_id: int) -> None:
        """Delete an agent."""
        agent = db.query(Agent).filter(Agent.id == agent_id).first()
        if not agent:
            raise ValueError(f"Agent {agent_id} not found")

        try:
            # Cleanup model resources
            await self.model_manager.cleanup_model(agent_id)
            
            # Delete agent
            db.delete(agent)
            db.commit()
            
            # Remove from active agents
            if agent_id in self.active_agents:
                del self.active_agents[agent_id]
        except Exception as e:
            db.rollback()
            raise ValueError(f"Failed to delete agent: {str(e)}")

    async def list_agents(
        self,
        db: Session,
        status: Optional[str] = None
    ) -> List[Agent]:
        """List all agents with optional status filter."""
        query = db.query(Agent)
        if status:
            query = query.filter(Agent.status == status)
        return query.all()

    async def process_message(
        self,
        agent_id: int,
        message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Process a message using the specified agent."""
        agent = self.active_agents.get(agent_id)
        if not agent:
            raise ValueError(f"Agent {agent_id} not found or inactive")

        try:
            response = await self.model_manager.generate_response(
                agent_id,
                message,
                context
            )
            return response
        except Exception as e:
            raise ValueError(f"Failed to process message: {str(e)}")