import os
from google.genai import types

def write_file(working_directory:str, file_path: str, content: str) -> str:
    try:
        work_dir = os.path.abspath(working_directory)
        targ_path = os.path.normpath(os.path.join(work_dir, file_path))
        if os.path.commonpath([targ_path, work_dir]) != work_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        elif os.path.isdir(file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        os.makedirs(os.path.dirname(targ_path), exist_ok=True)
        with open(targ_path, "w") as file:
            file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Overwrites a file with specified content into a specified file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write to, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file, if empty simply deletes all text in the file"
            )
        },
        required=["file_path", "content"]
    ),
)