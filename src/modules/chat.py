from openai import OpenAI
from .utils import restore_history, add_history, get_history
from .tools.tools import get_tools, get_tools_functions
import json

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

def chat(query: str):
    restore_history()
    history = get_history()
    
    messages = history
    messages.append({"role": "user", "content": query})
    
    tools = get_tools()
    tool_functions = get_tools_functions()
    
    while True:
        response = client.chat.completions.create(
            model="qwen2.5:7b-instruct-q5_0",
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0.1,
        )
        
        message = response.choices[0].message
        messages.append(message)
        
        if message.tool_calls:
            for tool_call in message.tool_calls:
                func_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                
                for tool_func in tool_functions:
                    if tool_func["name"] == func_name:
                        result = tool_func["callback"](**args)
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": result
                        })
                        break
        else:
            break
    
    final_response = message.content
    add_history("user", query)
    add_history("assistant", final_response)
    return final_response
