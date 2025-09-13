from functions.filesinfo import get_files_info
from functions.filescontent import get_file_content
from functions.writefile import write_file
from functions.runpyfile import run_python_file
from google.genai import types 

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"- Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f"- Calling function: {function_call_part.name}")
    
    wdir = "./calculator"
    args_obj = function_call_part.args or {}

    function_response = {}
    if function_call_part.name == "get_file_content":
        function_response["result"] = get_file_content(
            working_directory=wdir,
            file_path=args_obj.get("file_path", "")
        )
    elif function_call_part.name == "get_files_info":
        function_response["result"] = get_files_info(
            working_directory=wdir,
            directory=args_obj.get("directory", ".")
        ) 
    elif function_call_part.name == "run_python_file":
        function_response["result"] = run_python_file(
            working_directory=wdir, 
            file_path=args_obj.get("file_path", ""),
            args=args_obj.get("args", [])
        )
    elif function_call_part.name == "write_file":
        function_response["result"] = write_file(
            working_directory=wdir,
            file_path=args_obj.get("file_path", ""),
            content=args_obj.get("content", "")
        ) 
    else:
        function_response["error"] = f"Unknown function: {function_call_part.name}"

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response=function_response
            )
        ],
    )

