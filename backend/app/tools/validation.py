"""Validation tools for code and output inspection."""

from typing import Dict, Any, List
import ast
import re
from pylint import epylint
import black

class CodeValidationTool:
    """Tool for validating code quality and structure."""

    async def execute(
        self,
        code: str,
        language: str,
        validation_types: List[str] = None
    ) -> Dict[str, Any]:
        """Execute code validation."""
        if not validation_types:
            validation_types = ["syntax", "style", "security"]

        results = {}
        try:
            if "syntax" in validation_types:
                results["syntax"] = await self._validate_syntax(code, language)
            if "style" in validation_types:
                results["style"] = await self._validate_style(code, language)
            if "security" in validation_types:
                results["security"] = await self._validate_security(code, language)

            success = all(r.get("success", False) for r in results.values())
            return {
                "success": success,
                "results": results
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def _validate_syntax(self, code: str, language: str) -> Dict[str, Any]:
        """Validate code syntax."""
        if language == "python":
            try:
                ast.parse(code)
                return {
                    "success": True,
                    "message": "Syntax is valid"
                }
            except SyntaxError as e:
                return {
                    "success": False,
                    "error": str(e)
                }
        # Add support for other languages here
        return {
            "success": False,
            "error": f"Syntax validation not supported for {language}"
        }

    async def _validate_style(self, code: str, language: str) -> Dict[str, Any]:
        """Validate code style."""
        if language == "python":
            try:
                # Use black to check formatting
                formatted_code = black.format_str(code, mode=black.FileMode())
                style_issues = []
                
                if formatted_code != code:
                    style_issues.append("Code formatting does not match Black style")

                # Use pylint for additional style checks
                (pylint_stdout, pylint_stderr) = epylint.py_run(
                    code,
                    return_std=True
                )
                
                return {
                    "success": len(style_issues) == 0,
                    "issues": style_issues,
                    "pylint_output": pylint_stdout.getvalue()
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e)
                }
        return {
            "success": False,
            "error": f"Style validation not supported for {language}"
        }

    async def _validate_security(self, code: str, language: str) -> Dict[str, Any]:
        """Validate code security."""
        security_patterns = {
            "python": [
                r"eval\s*\(",
                r"exec\s*\(",
                r"os\.system\s*\(",
                r"subprocess\.call\s*\(",
                r"input\s*\(",
                r"__import__\s*\("
            ]
        }

        if language not in security_patterns:
            return {
                "success": False,
                "error": f"Security validation not supported for {language}"
            }

        issues = []
        for pattern in security_patterns[language]:
            if re.search(pattern, code):
                issues.append(f"Potentially unsafe pattern found: {pattern}")

        return {
            "success": len(issues) == 0,
            "issues": issues
        } 