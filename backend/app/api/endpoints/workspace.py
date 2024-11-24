"""Workspace management endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from ...core.file_context import FileContextManager
from ...db.session import get_db
from ...tools.filesystem import FileSystemTool
from ...core.config import settings

router = APIRouter()
filesystem_tool = FileSystemTool()

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    path: str = Form(...),
    db: Session = Depends(get_db)
):
    """Upload a file to workspace."""
    if file.size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds maximum limit"
        )

    try:
        content = await file.read()
        result = await filesystem_tool.execute(
            operation="write",
            path=f"{settings.WORKSPACE_DIR}/{path}",
            content=content.decode()
        )
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])
            
        return {
            "status": "success",
            "message": "File uploaded successfully",
            "path": path
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload file: {str(e)}"
        )

@router.get("/files")
async def list_files(
    path: str = "",
    db: Session = Depends(get_db)
):
    """List files in workspace directory."""
    try:
        result = await filesystem_tool.execute(
            operation="list",
            path=f"{settings.WORKSPACE_DIR}/{path}"
        )
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])
            
        return result["files"]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list files: {str(e)}"
        )

@router.delete("/files/{path:path}")
async def delete_file(
    path: str,
    db: Session = Depends(get_db)
):
    """Delete a file from workspace."""
    try:
        result = await filesystem_tool.execute(
            operation="delete",
            path=f"{settings.WORKSPACE_DIR}/{path}"
        )
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])
            
        return {
            "status": "success",
            "message": "File deleted successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete file: {str(e)}"
        )

@router.get("/files/{path:path}")
async def get_file_content(
    path: str,
    db: Session = Depends(get_db)
):
    """Get file content from workspace."""
    try:
        result = await filesystem_tool.execute(
            operation="read",
            path=f"{settings.WORKSPACE_DIR}/{path}"
        )
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])
            
        return {
            "content": result["content"],
            "path": path
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to read file: {str(e)}"
        ) 