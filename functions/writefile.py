import os 

def write_file(working_directory, file_path, content):
    try:
        target_file = os.path.join(working_directory, file_path)
        abs_target_file = os.path.abspath(target_file)
        abs_working_dir = os.path.abspath(working_directory)

        if os.path.commonpath([abs_working_dir, abs_target_file]) != abs_working_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        with open(abs_target_file, "w") as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'
        