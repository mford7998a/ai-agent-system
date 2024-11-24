"""Code execution tool for running and validating code."""

import subprocess
import tempfile
import os
from typing import Dict, Any
from pathlib import Path

class CodeExecutionTool:
    """Tool for executing code safely."""

    def __init__(self, workspace_dir: str):
        """Initialize code execution tool."""
        self.workspace_path = Path(workspace_dir)
        self.temp_dir = Path(tempfile.mkdtemp())

    async def execute(
        self,
        code: str,
        language: str,
        timeout: int = 30,
        env_vars: Dict[str, str] = None
    ) -> Dict[str, Any]:
        """Execute code in a safe environment."""
        try:
            file_path = self._create_temp_file(code, language)
            result = await self._run_code(file_path, language, timeout, env_vars)
            return result
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "output": None
            }
        finally:
            self._cleanup()

    def _create_temp_file(self, code: str, language: str) -> Path:
        """Create temporary file with code."""
        extensions = {
            "python": ".py",
            "javascript": ".js",
            "typescript": ".ts"
        }
        ext = extensions.get(language, ".txt")
        file_path = self.temp_dir / f"code{ext}"
        
        with open(file_path, "w") as f:
            f.write(code)
        
        return file_path

    async def _run_code(
        self,
        file_path: Path,
        language: str,
        timeout: int,
        env_vars: Dict[str, str] = None
    ) -> Dict[str, Any]:
        """Run code file with appropriate interpreter."""
        commands = {
            "python": ["python", str(file_path)],
            "javascript": ["node", str(file_path)],
            "typescript": ["ts-node", str(file_path)]
        }

        if language not in commands:
            return {
                "success": False,
                "error": f"Unsupported language: {language}",
                "output": None
            }

        try:
            env = os.environ.copy()
            if env_vars:
                env.update(env_vars)

            process = subprocess.Popen(
                commands[language],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                text=True
            )

            stdout, stderr = process.communicate(timeout=timeout)
            
            return {
                "success": process.returncode == 0,
                "error": stderr if stderr else None,
                "output": stdout
            }
        except subprocess.TimeoutExpired:
            process.kill()
            return {
                "success": False,
                "error": f"Execution timed out after {timeout} seconds",
                "output": None
            }

    def _cleanup(self):
        """Clean up temporary files."""
        try:
            for file in self.temp_dir.glob("*"):
                file.unlink()
        except Exception:
            pass 