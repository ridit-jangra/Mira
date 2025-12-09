import os
from pathlib import Path

def create_file(file_name: str, content: str = "", folder: str = "") -> str:
    try:
        if folder.strip():
            full_path = Path(folder) / file_name
            full_path.parent.mkdir(parents=True, exist_ok=True)  
        else:
            full_path = Path(file_name)
        
        with open(full_path, 'w') as f:
            f.write(content if content else "")
        
        return f"✅ File '{full_path}' created successfully with {len(content)} characters"
    except Exception as e:
        return f"❌ Failed to create file: {str(e)}"

tool = {
    "type": "function",
    "function": {
        "name": "create_file",
        "description": "Create a file with optional content in a specified folder. Auto-creates folders if they don't exist.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_name": {
                    "type": "string",
                    "description": "Name of the file to create (e.g., 'script.py', 'notes.txt')"
                },
                "content": {
                    "type": "string",
                    "description": "Optional content to write to the file. Leave empty for blank file."
                },
                "folder": {
                    "type": "string",
                    "description": "Optional folder path to create file in (e.g., 'src/utils', 'docs'). Creates if missing."
                }
            },
            "required": ["file_name"]
        }
    }
}

tool_function = {"name": "create_file", "callback": create_file}
