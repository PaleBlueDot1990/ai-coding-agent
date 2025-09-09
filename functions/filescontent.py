import os 

def get_file_content(working_directory, file_path):
    # `file_path` is a relative path within the `working_directory`
    try:
        target_file = os.path.join(working_directory, file_path)
        abs_target_file = os.path.abspath(target_file)
        abs_working_dir = os.path.abspath(working_directory)

        if os.path.commonpath([abs_working_dir, abs_target_file]) != abs_working_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(abs_target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        file_content = None 
        MAX_CHARS = 10000
        APPEND_MESSAGE = f'...File "{file_path}" truncated at 10000 characters'
        with open(abs_target_file, "r") as f:
            file_content = f.read(MAX_CHARS)
            extra = f.read(1)  
            if extra:  
                file_content += APPEND_MESSAGE
        return file_content
    except Exception as e:
        return f'Error: {e}'

        
    

