"""API router configuration."""

from fastapi import APIRouter

from ..endpoints import (
    agents,
    chat,
    file_context,
    group_chat,
    model_providers,
    tasks,
    tools,
    workspace
)

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(file_context.router, prefix="/file-context", tags=["file-context"])
api_router.include_router(group_chat.router, prefix="/group-chat", tags=["group-chat"])
api_router.include_router(model_providers.router, prefix="/model-providers", tags=["model-providers"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(tools.router, prefix="/tools", tags=["tools"])
api_router.include_router(workspace.router, prefix="/workspace", tags=["workspace"]) 