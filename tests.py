from functions.filesinfo import get_files_info
from functions.filescontent import get_file_content
from functions.writefile import write_file
from functions.runpyfile import run_python_file

def main():
    print(run_python_file("calculator", "main.py"))
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print(run_python_file("calculator", "tests.py"))
    print(run_python_file("calculator", "../main.py"))
    print(run_python_file("calculator", "nonexistent.py"))

if __name__ == "__main__":
    main()