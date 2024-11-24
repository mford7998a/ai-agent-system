from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, JSON

from ..db.base import Base

class FileContext(Base):
    """File context model."""
    
    __tablename__ = "file_contexts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    file_path = Column(String)
    content = Column(String)
    status = Column(String, default="active")
    metadata = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 