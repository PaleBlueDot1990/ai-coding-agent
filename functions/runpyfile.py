import os 
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    try:
        target_file = os.path.join(working_directory, file_path)
        abs_target_file = os.path.abspath(target_file)
        abs_working_dir = os.path.abspath(working_directory)

        if os.path.commonpath([abs_working_dir, abs_target_file]) != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(abs_target_file):
            return f'Error: File "{file_path}" not found.'
        
        if file_path.split(".")[-1] != "py":
            f'Error: "{file_path}" is not a Python file.'
        
        subprocess_args = ["python3", abs_target_file]
        subprocess_args.extend(args)

        result = subprocess.run(
            args=subprocess_args, 
            timeout=30, 
            cwd=abs_working_dir,  
            capture_output=True,
            text=True
        )

        if not result.stdout and not result.stderr:
            return "No output produced\n" 
               
        output = f"STDOUT:\n{result.stdout}\n"
        output += f"STDERR:\n{result.stderr}\n"
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}\n"
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
