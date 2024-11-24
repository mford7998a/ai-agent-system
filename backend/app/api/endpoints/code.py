from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from ...tools.code_execution import CodeExecutionTool
from ...tools.filesystem import FileSystemTool

router = APIRouter()
code_execution_tool = CodeExecutionTool()
filesystem_tool = FileSystemTool()

@router.post("/execute")
async def execute_code(data: Dict[str, Any]):
    result = await code_execution_tool.execute(
        code=data.get("content"),
        language=data.get("language", "python")
    )
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result

@router.put("/files/{file_id}")
async def save_code(file_id: str, data: Dict[str, Any]):
    result = await filesystem_tool.execute(
        operation="write",
        path=f"code/{file_id}",
        content=data.get("content")
    )
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result

@router.get("/files/{file_id}")
async def get_code(file_id: str):
    result = await filesystem_tool.execute(
        operation="read",
        path=f"code/{file_id}"
    )
    
    if not result["success"]:
        raise HTTPException(status_code=404, detail=result["error"])
    
    return result 