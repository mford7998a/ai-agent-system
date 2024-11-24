"""File context management endpoints."""

import json
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from ...core.file_context import FileContextManager
from ...db.session import get_db
from ...models.file_context import FileContext
from ...schemas.file_context import (
    FileContextCreate,
    FileContextResponse,
    FileContextUpdate
)
from ...tools.filesystem import FileSystemTool

router = APIRouter()
filesystem_tool = FileSystemTool()

@router.post("/", response_model=FileContextResponse)
async def create_file_context(
    context_data: FileContextCreate,
    db: Session = Depends(get_db)
) -> FileContextResponse:
    """Create a new file context."""
    manager = FileContextManager(db, "workspace")
    try:
        context = await manager.add_file_context(
            name=context_data.name,
            file_path=context_data.file_path,
            content=context_data.content,
            metadata=context_data.metadata
        )
        return context
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/upload")
async def upload_file_context(
    file: UploadFile = File(...),
    name: str = Form(...),
    metadata: str = Form("{}"),
    db: Session = Depends(get_db)
):
    """Upload a file and create a file context."""
    content = await file.read()
    file_path = f"contexts/{file.filename}"
    
    # Save file to workspace
    result = await filesystem_tool.execute(
        operation="write",
        path=file_path,
        content=content.decode()
    )
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    
    try:
        # Create database record
        context = FileContext(
            name=name,
            file_path=file_path,
            content=content.decode(),
            metadata=json.loads(metadata)
        )
        
        db.add(context)
        db.commit()
        db.refresh(context)
        
        return context
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create file context: {str(e)}"
        )

@router.get("/{context_id}/content")
async def get_file_content(context_id: int, db: Session = Depends(get_db)):
    manager = FileContextManager(db, "workspace")
    try:
        return await manager.get_file_content(context_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{context_id}")
async def update_file_context(
    context_id: int,
    context_update: FileContextUpdate,
    db: Session = Depends(get_db)
):
    manager = FileContextManager(db, "workspace")
    try:
        return await manager.update_file_content(
            context_id=context_id,
            content=context_update.content,
            metadata_updates=context_update.metadata
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{context_id}")
async def delete_file_context(context_id: int, db: Session = Depends(get_db)):
    manager = FileContextManager(db, "workspace")
    try:
        await manager.delete_file_context(context_id)
        return {"status": "success", "message": "File context deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/", response_model=List[FileContextResponse])
async def list_file_contexts(
    status: str = "active",
    db: Session = Depends(get_db)
):
    manager = FileContextManager(db, "workspace")
    return await manager.list_contexts(status) 