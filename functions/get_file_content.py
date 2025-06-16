import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    working_path = os.path.abspath(working_directory)
    file_abs_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not file_abs_path.startswith(working_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(file_abs_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(file_abs_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
    
        if len(file_content_string) == MAX_CHARS:
            file_content_string += f' [...File "{file_path}" truncated at 10000 characters]'
        
        return file_content_string
    except Exception as e:
        return f'Error: reading file {file_path}: {e}'
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the file in the specified directory and returns its content, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read and return content, relative to the working directory.",
            ),
        },
    ),
)