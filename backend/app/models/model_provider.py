from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, JSON, Boolean
from sqlalchemy.orm import relationship

from ..db.base import Base

class ModelProvider(Base):
    """Model provider model."""
    
    __tablename__ = "model_providers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    api_key = Column(String)
    base_url = Column(String)
    is_active = Column(Boolean, default=True)
    supported_models = Column(JSON, default=[])
    config = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    custom_agents = relationship("CustomAgent", back_populates="model_provider")