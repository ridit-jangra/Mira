import pathlib
import tempfile
import os
import json

path = pathlib.Path()
history_folder_path = path.joinpath(tempfile.gettempdir(), "mira", "history")
history_file_path = path.joinpath(history_folder_path, "mira.json")

if not os.path.exists(history_folder_path):
    os.makedirs(history_folder_path, exist_ok=True)

history = []

def add_history(role: str, message: str):
    history.append({"role": role, "content": message})
    with open(history_file_path, "w") as f:
        json.dump(history, f, indent=2)

def get_history():
    global history
    return history.copy()

def restore_history():
    global history
    if os.path.exists(history_file_path):
        try:
            with open(history_file_path, "r") as f:
                content = f.read().strip()
                if content:  
                    history = json.loads(content)
                else:
                    history = []  
        except (json.JSONDecodeError, ValueError):
            print("Corrupted history file, resetting...")
            history = []  


def clear_history():
    global history
    if os.path.exists(history_file_path):
        with open(history_file_path, "w") as f:
            f.write("")
            history = []