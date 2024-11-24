"""Tool management endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...core.tool_manager import ToolManager
from ...db.session import get_db
from ...models.tool import Tool
from ...schemas.tool import ToolCreate, ToolResponse, ToolUpdate

router = APIRouter()
tool_manager = ToolManager()

@router.post("/", response_model=ToolResponse)
async def create_tool(
    tool_data: ToolCreate,
    db: Session = Depends(get_db)
) -> ToolResponse:
    """Create a new tool."""
    try:
        tool = Tool(**tool_data.dict())
        db.add(tool)
        db.commit()
        db.refresh(tool)
        
        # Register tool if available
        if tool.is_available:
            await tool_manager.register_tool(tool)
            
        return tool
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Failed to create tool: {str(e)}"
        )

@router.get("/{tool_id}", response_model=ToolResponse)
async def get_tool(tool_id: int, db: Session = Depends(get_db)) -> ToolResponse:
    """Get tool by ID."""
    tool = await tool_manager.get_tool(tool_id)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    return tool

@router.put("/{tool_id}", response_model=ToolResponse)
async def update_tool(
    tool_id: int,
    tool_data: ToolUpdate,
    db: Session = Depends(get_db)
) -> ToolResponse:
    """Update a tool."""
    tool = db.query(Tool).filter(Tool.id == tool_id).first()
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
        
    try:
        # Update tool attributes
        for field, value in tool_data.dict(exclude_unset=True).items():
            setattr(tool, field, value)
            
        db.commit()
        db.refresh(tool)
        
        # Update tool registration status
        if tool.is_available:
            await tool_manager.register_tool(tool)
        else:
            await tool_manager.unregister_tool(tool_id)
            
        return tool
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Failed to update tool: {str(e)}"
        )

@router.delete("/{tool_id}")
async def delete_tool(tool_id: int, db: Session = Depends(get_db)):
    """Delete a tool."""
    tool = db.query(Tool).filter(Tool.id == tool_id).first()
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
        
    try:
        # Unregister tool
        await tool_manager.unregister_tool(tool_id)
        
        # Delete from database
        db.delete(tool)
        db.commit()
        return {"status": "success", "message": "Tool deleted"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Failed to delete tool: {str(e)}"
        )

@router.get("/", response_model=List[ToolResponse])
async def list_tools(
    available_only: bool = False,
    db: Session = Depends(get_db)
) -> List[ToolResponse]:
    """List all tools."""
    query = db.query(Tool)
    if available_only:
        query = query.filter(Tool.is_available == True)
    return query.all()

@router.post("/{tool_id}/execute")
async def execute_tool(
    tool_id: int,
    params: dict,
    db: Session = Depends(get_db)
):
    """Execute a tool with given parameters."""
    tool = await tool_manager.get_tool(tool_id)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
        
    try:
        result = await tool_manager.execute_tool(tool, params)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) 