from pathlib import Path
from loguru import logger

from app.schema import Tool, ToolCall, ToolResult
from app.tool.base import BaseTool


class FileSaver(BaseTool):
    """Tool for saving data to files."""

    def __init__(self):
        super().__init__(
            name="FileSaver",
            description="Saves data to files",
            parameters={
                "type": "object",
                "properties": {
                    "data": {
                        "type": "object",
                        "description": "The DataFrame to save",
                    },
                    "file_path": {
                        "type": "string",
                        "description": "Path where to save the file",
                    },
                    "index": {
                        "type": "boolean",
                        "description": "Whether to save the index",
                        "default": False,
                    },
                },
                "required": ["data", "file_path"],
            },
        )

    async def _call(self, tool_call: ToolCall) -> ToolResult:
        """Save data to a file."""
        try:
            data = tool_call.arguments["data"]
            file_path = tool_call.arguments["file_path"]
            index = tool_call.arguments.get("index", False)
            
            # Create directory if it doesn't exist
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Save the data
            data.to_csv(file_path, index=index)
            logger.info(f"Successfully saved data to {file_path}")
            
            return ToolResult(
                success=True,
                data={"file_path": file_path},
            )

        except Exception as e:
            logger.error(f"Error saving data: {str(e)}")
            return ToolResult(success=False, error=str(e))
