import os 
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself."
            )
        }
    )
)

def get_files_info(working_directory, directory="."):
    # `directory` is a relative path within the `working_directory`

    try:
        target_directory = os.path.join(working_directory, directory)
        abs_working_dir = os.path.abspath(working_directory)
        abs_target_dir = os.path.abspath(target_directory)

        if os.path.commonpath([abs_working_dir, abs_target_dir]) != abs_working_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
        if not os.path.isdir(abs_target_dir):
            return f'Error: "{abs_target_dir}" is not a directory'

        file_info = ""
        for name in os.listdir(abs_target_dir):
            path = os.path.join(abs_target_dir, name)
            is_dir = os.path.isdir(path)            
            size = get_directory_size_r(path)
            file_info += f"- {path[len(abs_target_dir)+1:]}: file_size={size} bytes, is_dir={is_dir}\n"
        return file_info
    except Exception as e:
        return f'Error: {e}'


def get_directory_size_r(path):
    if os.path.isfile(path):
        return os.path.getsize(path)
    
    total_size = 0
    for name in os.listdir(path):
        sub_path = os.path.join(path, name)
        total_size += get_directory_size_r(sub_path)
    return total_size

