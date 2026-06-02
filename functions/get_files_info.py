import os
from google.genai import types

def get_files_info(working_directory: str, directory: str=".") -> str:
    try:
        if not os.path.isdir(os.path.join(working_directory, directory)):
            return f'Error: "{directory}" is not a directory'
        work_dir = os.path.abspath(working_directory)
        targ_path = os.path.normpath(os.path.join(work_dir, directory))
        if os.path.commonpath([targ_path, work_dir]) != work_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        else:
            subdir = os.listdir(targ_path)
            lines = []
            for dir in subdir:
                if dir != "__pycache__":
                    size = os.path.getsize(os.path.join(targ_path, dir))
                    isdir = os.path.isdir(os.path.join(targ_path, dir))
                    lines.append(f"- {dir}: file_size={size} bytes, is_dir={isdir}")
            return "\n ".join(lines)


            #return f'Success: "{directory}" is within the working directory'
    except Exception as e:
        return f"Error: {e}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)