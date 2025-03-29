import pandas as pd
from pathlib import Path
from loguru import logger

from app.schema import Tool, ToolCall, ToolResult
from app.tool.base import BaseTool


class DataCollector(BaseTool):
    """Tool for collecting data from CSV files."""

    def __init__(self):
        super().__init__(
            name="DataCollector",
            description="Collects data from CSV files",
            parameters={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the CSV file",
                    },
                    "encoding": {
                        "type": "string",
                        "description": "File encoding (default: utf-8)",
                        "default": "utf-8",
                    },
                },
                "required": ["file_path"],
            },
        )

    async def _call(self, tool_call: ToolCall) -> ToolResult:
        """Load data from a CSV file."""
        try:
            file_path = tool_call.arguments["file_path"]
            encoding = tool_call.arguments.get("encoding", "utf-8")
            
            # Ensure file exists
            if not Path(file_path).exists():
                return ToolResult(
                    success=False,
                    error=f"File not found: {file_path}",
                )
            
            # Load the data
            data = pd.read_csv(file_path, encoding=encoding)
            logger.info(f"Successfully loaded {len(data)} rows from {file_path}")
            
            return ToolResult(
                success=True,
                data={"data": data},
            )

        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            return ToolResult(success=False, error=str(e)) 