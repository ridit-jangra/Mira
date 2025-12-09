import os
from pathlib import Path

def create_folder(folder_name: str):
    try:
        if os.path.exists(folder_name):
            return "Folder already exists"
        os.mkdir(folder_name)
        return f"✅ Folder '{folder_name}' created successfully"
    except Exception as e:
        return f"❌ Failed to create folder: {str(e)}"

tool = {
    "type": "function",
    "function": {
        "name": "create_folder",
        "description": "Create a folder with name specificed by the user",
        "parameters": {
            "type": "object",
            "properties": {
                "folder_name": {
                    "type": "string",
                    "description": "Name of the folder to create (e.g., 'script', 'notes')"
                }
            },
            "required": ["folder_name"]
        }
    }
}

tool_function = {"name": "create_folder", "callback": create_folder}
