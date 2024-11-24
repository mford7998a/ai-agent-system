"""Code execution engine for running and validating code."""

import subprocess
import tempfile
import os
import shutil
from typing import Dict, Any
from pathlib import Path

class ExecutionEngine:
    """Engine for executing code in a sandboxed environment."""

    def __init__(self):
        """Initialize execution engine."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.supported_languages = {
            "python": {
                "extension": ".py",
                "command": ["python"],
                "timeout": 30
            },
            "javascript": {
                "extension": ".js",
                "command": ["node"],
                "timeout": 30
            },
            "typescript": {
                "extension": ".ts",
                "command": ["ts-node"],
                "timeout": 30
            }
        }

    async def execute_code(
        self,
        code: str,
        language: str,
        env_vars: Dict[str, str] = None
    ) -> Dict[str, Any]:
        """Execute code in a sandboxed environment."""
        if language not in self.supported_languages:
            return {
                "success": False,
                "error": f"Unsupported language: {language}",
                "output": None
            }

        try:
            # Create temporary file
            lang_config = self.supported_languages[language]
            file_path = self.temp_dir / f"code{lang_config['extension']}"
            with open(file_path, "w") as f:
                f.write(code)

            # Prepare environment
            env = os.environ.copy()
            if env_vars:
                env.update(env_vars)

            # Execute code
            process = subprocess.Popen(
                [*lang_config["command"], str(file_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                text=True
            )

            try:
                stdout, stderr = process.communicate(timeout=lang_config["timeout"])
                return {
                    "success": process.returncode == 0,
                    "error": stderr if stderr else None,
                    "output": stdout
                }
            except subprocess.TimeoutExpired:
                process.kill()
                return {
                    "success": False,
                    "error": f"Execution timed out after {lang_config['timeout']} seconds",
                    "output": None
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "output": None
            }
        finally:
            # Cleanup
            if file_path.exists():
                file_path.unlink()

    def cleanup(self):
        """Clean up temporary files."""
        try:
            shutil.rmtree(self.temp_dir)
        except Exception:
            pass