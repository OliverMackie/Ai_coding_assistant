import os
from google.genai import types

def get_file_content(working_directory:str, file_path:str) -> str:
    try:
        work_dir = os.path.abspath(working_directory)
        targ_path = os.path.normpath(os.path.join(work_dir, file_path))
        if os.path.commonpath([targ_path, work_dir]) != work_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(targ_path):
            return f'Error: File not found or is not a regular file. "{file_path}"'
        else:
            with open(targ_path) as file:
                file_str = file.read(10000)
                if file.read(1):
                    file_str += f'[... File "{file_path}]" truncated at 10000 characters'
                return file_str
    except Exception as e:
        return f"Error: {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads up to 10000 characters in a specified file relative to the working directory, sometimes with a suffix stating that the file was truncated",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to read from, relative to the working directory",
            ),
        },
        required=["file_path"]
    ),
)