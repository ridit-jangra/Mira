from .create_file import tool as tool_create_file, tool_function as tool_function_create_file
from .run_command import tool as tool_run_command, tool_function as tool_function_run_command
from .create_folder import tool as tool_create_folder, tool_function as tool_function_create_folder

tools = [tool_create_file, tool_run_command, tool_create_folder]
tools_functions = [tool_function_create_file, tool_function_run_command, tool_function_create_folder]

def get_tools():
    return tools

def get_tools_functions():
    return tools_functions
