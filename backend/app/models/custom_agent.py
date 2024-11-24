from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, JSON, Float
from sqlalchemy.orm import relationship

from ..db.base import Base

class CustomAgent(Base):
    """Custom agent model."""
    
    __tablename__ = "custom_agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    system_prompt = Column(String)
    model_provider_id = Column(Integer, ForeignKey("model_providers.id"))
    model_name = Column(String)
    temperature = Column(Float, default=0.7)
    tools = Column(JSON, default=[])
    metadata = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    model_provider = relationship("ModelProvider", back_populates="custom_agents")