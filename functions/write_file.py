import os
from google.genai import types

def write_file(working_directory, file_path, content):
    working_path = os.path.abspath(working_directory)
    file_abs_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not file_abs_path.startswith(working_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    

    if not os.path.exists(file_abs_path):
        try:
            os.makedirs(os.path.dirname(file_abs_path), exist_ok=True)
        except Exception as e:
            return f'Error: creating directory: {e}'

    if os.path.exists(file_abs_path) and os.path.isdir(file_abs_path):
        return f'Error: "{file_path}" is a directory, not a file'

    try:
        with open(file_abs_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: writing content to {file_path}: {e}'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrites file in the specified directory with the given content, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write or overwrite with content, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write or overwrite the file with.",
            ),
        },
    ),
)
