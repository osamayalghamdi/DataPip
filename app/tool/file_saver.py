import os

import aiofiles

from app.tool.base import BaseTool


class FileSaver(BaseTool):
    name: str = "file_saver"
    description: str = """Save content to a file that I will provide to you under folder called output.
Use this tool when you need to save text, code, or generated content to a the path I give it to you.
The tool accepts content and a file path, and saves the content to that location.
"""
    parameters: dict = {
        "type": "object",
        "properties": {
            "content": {
                "type": "string",
                "description": "(required) The content to save to the file.",
            },
            "file_path": {
                "type": "string",
                "description": "(required) The path where the file should be saved, including filename and extension.",
            },
            "mode": {
                "type": "string",
                "description": "(optional) The file opening mode. Default is 'w' for write. Use 'a' for append.",
                "enum": ["w", "a"],
                "default": "w",
            },
        },
        "required": ["content", "file_path"],
    }

    async def execute(self, content: str, file_path: str, mode: str = "w") -> str:
        """
        Save content to a file at the specified path.

        Args:
            content (str): The content to save to the file.
            file_path (str): The path where the file should be saved.
            mode (str, optional): The file opening mode. Default is 'w' for write. Use 'a' for append.

        Returns:
            str: A message indicating the result of the operation.
        """
        try:
            # Define project root directory
            project_dir = r"C:\IT\personalProjects\DataPip\Output"
            
            # If file_path is absolute, check if it's within project directory
            if os.path.isabs(file_path):
                if not file_path.startswith(project_dir):
                    # Force the path to be within project directory
                    file_path = os.path.join(project_dir, os.path.basename(file_path))
            else:
                # If relative path, make it relative to project directory
                file_path = os.path.join(project_dir, file_path)
            
            path = os.path.abspath(file_path)
            
            # Ensure the directory exists
            directory = os.path.dirname(path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)

            # Write directly to the file
            async with aiofiles.open(path, mode, encoding="utf-8") as file:
                await file.write(content)

            return f"Content successfully saved to {path}"
        except Exception as e:
            return f"Error saving file: {str(e)}"
