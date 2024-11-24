"""File context manager for handling file operations."""

import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from ..models.file_context import FileContext
from ..tools.filesystem import FileSystemTool

class FileContextManager:
    """Manager class for file context operations."""

    def __init__(self, db: Session, workspace_dir: str):
        """Initialize file context manager."""
        self.db = db
        self.workspace_path = Path(workspace_dir)
        self.fs_tool = FileSystemTool()
        os.makedirs(workspace_dir, exist_ok=True)

    async def add_file_context(
        self,
        name: str,
        file_path: str,
        content: str,
        metadata: Dict[str, Any]
    ) -> FileContext:
        """Add a new file context."""
        try:
            # Save file to workspace
            full_path = self.workspace_path / file_path
            await self.fs_tool.execute(
                operation="write",
                path=str(full_path),
                content=content
            )
            
            # Create database record
            context = FileContext(
                name=name,
                file_path=file_path,
                content=content,
                metadata=metadata
            )
            self.db.add(context)
            self.db.commit()
            self.db.refresh(context)
            
            return context
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Failed to create file context: {str(e)}")

    async def get_file_content(self, context_id: int) -> Dict[str, Any]:
        """Get file content by context ID."""
        context = self.db.query(FileContext).filter(FileContext.id == context_id).first()
        if not context:
            raise ValueError(f"Context {context_id} not found")
            
        full_path = self.workspace_path / context.file_path
        result = await self.fs_tool.execute(
            operation="read",
            path=str(full_path)
        )
        
        if not result["success"]:
            raise ValueError(f"Failed to read file: {result['error']}")
            
        return {
            "content": result["content"],
            "metadata": context.metadata,
            "file_path": context.file_path
        }

    async def update_file_content(
        self,
        context_id: int,
        content: Optional[str] = None,
        metadata_updates: Optional[Dict[str, Any]] = None
    ) -> FileContext:
        """Update file content and/or metadata."""
        context = self.db.query(FileContext).filter(FileContext.id == context_id).first()
        if not context:
            raise ValueError(f"Context {context_id} not found")
            
        try:
            if content is not None:
                full_path = self.workspace_path / context.file_path
                result = await self.fs_tool.execute(
                    operation="write",
                    path=str(full_path),
                    content=content
                )
                if not result["success"]:
                    raise ValueError(f"Failed to write file: {result['error']}")
                context.content = content
            
            if metadata_updates:
                context.metadata.update(metadata_updates)
                
            context.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(context)
            
            return context
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Failed to update file context: {str(e)}")

    async def delete_file_context(self, context_id: int) -> None:
        """Delete a file context and its associated file."""
        context = self.db.query(FileContext).filter(FileContext.id == context_id).first()
        if not context:
            raise ValueError(f"Context {context_id} not found")
            
        try:
            # Delete file from workspace
            full_path = self.workspace_path / context.file_path
            await self.fs_tool.execute(
                operation="delete",
                path=str(full_path)
            )
            
            # Delete database record
            self.db.delete(context)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Failed to delete file context: {str(e)}")

    async def list_contexts(self, status: str = "active") -> List[FileContext]:
        """List all file contexts with given status."""
        query = self.db.query(FileContext)
        if status:
            query = query.filter(FileContext.status == status)
        return query.all() 