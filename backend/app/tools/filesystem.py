import os
from pathlib import Path
from typing import Dict, Any

class FileSystemTool:
    """Tool for filesystem operations."""

    async def execute(
        self,
        operation: str,
        path: str,
        content: str = None
    ) -> Dict[str, Any]:
        """Execute filesystem operation."""
        try:
            if operation == "read":
                return await self._read_file(path)
            elif operation == "write":
                return await self._write_file(path, content)
            elif operation == "delete":
                return await self._delete_file(path)
            else:
                return {
                    "success": False,
                    "error": f"Unsupported operation: {operation}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def _read_file(self, path: str) -> Dict[str, Any]:
        """Read file content."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            return {
                "success": True,
                "content": content
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to read file: {str(e)}"
            }

    async def _write_file(self, path: str, content: str) -> Dict[str, Any]:
        """Write content to file."""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(path), exist_ok=True)
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return {
                "success": True
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to write file: {str(e)}"
            }

    async def _delete_file(self, path: str) -> Dict[str, Any]:
        """Delete file."""
        try:
            if os.path.exists(path):
                os.remove(path)
                return {
                    "success": True
                }
            return {
                "success": False,
                "error": "File not found"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to delete file: {str(e)}"
            } 