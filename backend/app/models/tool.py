from typing import Optional, Dict, Any, Type
from sqlalchemy import Column, String, JSON, Integer, Table, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from .base import TimeStampedBase
import importlib
from importlib.util import find_spec
from datetime import datetime

tool_configs = Table(
    'tool_configs',
    TimeStampedBase.metadata,
    Column('agent_id', Integer, ForeignKey('agents.id', ondelete='CASCADE')),
    Column('tool_id', Integer, ForeignKey('tools.id', ondelete='CASCADE')),
    Column('config', JSON, nullable=False, server_default='{}')
)

class Tool(TimeStampedBase):
    """Tool model representing available tools for agents."""
    
    __tablename__ = "tools"

    # Required fields
    name: str = Column(String(100), index=True, unique=True, nullable=False)
    description: Optional[str] = Column(String(500), nullable=True)
    tool_type: str = Column(String(50), nullable=False)
    config_schema: Dict[str, Any] = Column(
        JSON,
        nullable=False,
        server_default='{"type":"object","properties":{},"required":[]}'
    )
    default_config: Dict[str, Any] = Column(
        JSON,
        nullable=False,
        server_default='{}'
    )
    is_system: bool = Column(
        Boolean,
        nullable=False,
        default=False,
        server_default='false'
    )
    is_available: bool = Column(Boolean, default=True)
    metadata: Dict[str, Any] = Column(JSON, default={})
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    agents = relationship(
        "Agent",
        secondary=tool_configs,
        back_populates="tools",
        cascade="all, delete",
        lazy="joined",
        collection_class=set
    )

    def __init__(self, **kwargs: Any) -> None:
        """Initialize a Tool instance with provided kwargs."""
        super().__init__(**kwargs)
        if not self.config_schema:
            self.config_schema = {
                "type": "object",
                "properties": {},
                "required": []
            }
        if not self.default_config:
            self.default_config = {}

    @property
    def is_available(self) -> bool:
        """Check if the tool implementation is available for use."""
        try:
            module_path: str = f"..tools.{self.tool_type}"
            return bool(find_spec(module_path))
        except ImportError:
            return False

    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate tool configuration against schema.
        
        Args:
            config: Configuration dictionary to validate.
            
        Returns:
            bool: True if configuration is valid, False otherwise.
        """
        from jsonschema import validate, ValidationError
        try:
            validate(instance=config, schema=self.config_schema)
            return True
        except ValidationError:
            return False

    def get_implementation(self) -> Optional[Type]:
        """Get the tool implementation class."""
        try:
            module = importlib.import_module(f"..tools.{self.tool_type}", package=__package__)
            return getattr(module, self.__class__.__name__)
        except (ImportError, AttributeError):
            return None

    def __repr__(self) -> str:
        """Return string representation of the Tool."""
        return f"<Tool(id={self.id}, name='{self.name}', type='{self.tool_type}')>"