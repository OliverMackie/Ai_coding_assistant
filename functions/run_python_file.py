import os
import subprocess

def run_python_file(
    working_directory: str,
    file_path: str,
    args: list[str] | None = None) -> str:
    try:
        work_dir = os.path.abspath(working_directory)
        targ_path = os.path.normpath(os.path.join(work_dir, file_path))
        if os.path.commonpath([targ_path, work_dir]) != work_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(targ_path):
            return f'Error: "{file_path}" does not exist or is not a regular file.'
        elif not targ_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        else:
            command = ["python", targ_path]
            if args != None:
                command.extend(args)
            process = subprocess.run(command, cwd=work_dir, capture_output=True, text=True, timeout=30)
            return_string = ""
            if process.returncode != 0:
                return_string += f"Process exited with code {process.returncode}"
            if (not process.stderr) and (not process.stdout):
                return_string += "No output produced"
            else:
                if process.stdout != None:  
                    return_string += f"STDOUT:\n{process.stdout}"
                if process.stderr != None: 
                    return_string += f"STDERR:\n{process.stderr}"
            return return_string
    except Exception as e:
        return f"Error: executing python file: {e}"