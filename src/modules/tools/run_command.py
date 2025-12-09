import os
import subprocess
import sys
from pathlib import Path

def run_command(command: str) -> str:
    """
    Execute ANY command with LIVE real-time output streaming + smart detection.
    """
    try:
        # Smart file detection & opening (non-blocking)
        if command.startswith(("run ", "open ", "execute ")):
            file_path = command.replace("run ", "").replace("open ", "").replace("execute ", "").strip()
            path = Path(file_path).expanduser()  # Handle ~/
            if path.exists():
                print(f"🔄 Running: {path.name}...")
                return open_file_smart(path)
            else:
                return f"❌ File not found: {file_path}"
        
        # Package installation with live output
        if any(x in command.lower() for x in ["pip install", "install ", "npm install"]):
            print(f"📦 LIVE Installing: {command}")
            return install_package_live(command)
        
        # Sudo commands
        if any(sudo_cmd in command.lower() for sudo_cmd in ["sudo ", "apt ", "pacman ", "yum "]):
            print(f"🔐 LIVE Sudo: {command}")
            return execute_sudo_live(command)
        
        # ALL OTHER COMMANDS - LIVE STREAMING
        print(f"▶️  LIVE: `{command}`")
        print("=" * 70)
        result = execute_live(command)
        print("=" * 70)
        return result
        
    except subprocess.TimeoutExpired:
        return f"⏰ `{command}` timed out after 30s"
    except KeyboardInterrupt:
        return "⏹️ Cancelled by user (Ctrl+C)"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def execute_live(command: str, timeout: int = 30) -> str:
    """Execute command with LIVE output streaming."""
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        output_lines = []
        for line in iter(process.stdout.readline, ''):
            if line:
                print(line.strip())
                output_lines.append(line.strip())
            if process.poll() is not None:
                break
        
        returncode = process.poll()
        stdout, stderr = process.communicate(timeout=timeout)
        
        if returncode == 0:
            return f"✅ `{command}` ✓\nLast 3 lines:\n" + "\n".join(output_lines[-3:])
        else:
            return f"❌ `{command}` failed (code {returncode})\nLast 3 lines:\n" + "\n".join(output_lines[-3:])
            
    except subprocess.TimeoutExpired:
        process.kill()
        return f"⏰ `{command}` timed out"
    except Exception as e:
        return f"❌ Live execution error: {str(e)}"

def install_package_live(command: str) -> str:
    """Install packages with live streaming."""
    print("=" * 70)
    result = execute_live(command, timeout=120)
    print("=" * 70)
    return result

def execute_sudo_live(command: str) -> str:
    """Execute sudo commands with live streaming."""
    print("=" * 70)
    result = execute_live(command, timeout=60)
    print("=" * 70)
    return result

def open_file_smart(file_path: Path) -> str:
    """Smart file opening by extension."""
    if not file_path.exists():
        return f"❌ File not found: {file_path}"
    
    # Arch Linux / Cross-platform handlers
    handlers = {
        # Scripts
        '.py': ['python3', str(file_path)],
        '.js': ['node', str(file_path)],
        '.ts': ['ts-node', str(file_path)],
        '.sh': ['bash', str(file_path)],
        '.bat': ['cmd', '/c', str(file_path)],
        
        # Editors
        '.txt': ['nano', str(file_path)],
        '.md': ['code', str(file_path)],
        '.json': ['code', str(file_path)],
        '.yaml': ['code', str(file_path)],
        '.yml': ['code', str(file_path)],
        
        # Web
        '.html': ['firefox', str(file_path)],
        '.css': ['firefox', str(file_path)],
        
        # Images
        '.png': ['eog', str(file_path)],
        '.jpg': ['eog', str(file_path)],
        '.jpeg': ['eog', str(file_path)],
        '.gif': ['eog', str(file_path)],
        '.svg': ['firefox', str(file_path)],
        
        # Media
        '.mp4': ['mpv', str(file_path)],
        '.avi': ['mpv', str(file_path)],
        '.mkv': ['mpv', str(file_path)],
        '.mp3': ['mpv', str(file_path)],
        
        # Docs
        '.pdf': ['zathura', str(file_path)],
        '.docx': ['libreoffice', str(file_path)],
    }
    
    ext = file_path.suffix.lower()
    if ext in handlers:
        subprocess.Popen(handlers[ext], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return f"✅ Launched {file_path.name} with {handlers[ext][0]}"
    
    # Universal fallback
    subprocess.Popen(['xdg-open', str(file_path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return f"✅ Opened {file_path.name} with default app (xdg-open)"

# TOOL DEFINITION for Ollama
tool = {
    "type": "function",
    "function": {
        "name": "run_command",
        "description": "Execute ANY shell command with LIVE real-time output. Auto-opens files smartly, installs packages, handles sudo. Say 'run file.py', 'pip install flask', 'sudo pacman -S htop', 'ls -la', etc.",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "Any command: 'run window.py', 'open image.png', 'pip install flask', 'sudo pacman -S firefox', 'flask run', 'git status', etc."
                }
            },
            "required": ["command"]
        }
    }
}

tool_function = {"name": "run_command", "callback": run_command}
