import os
from google.genai import types

def get_files_info(working_directory, directory=None):

    working_path = os.path.abspath(working_directory)

    directory_path = working_path
    if directory:
        directory_path = os.path.abspath(os.path.join(working_directory, directory))

    if not directory_path.startswith(working_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(directory_path):
        return f'Error: "{directory}" is not a directory'

    try:
        files_info = []
        dir_list = os.listdir(directory_path)
        for item in dir_list:
            if item.startswith("__"):
                continue
            path = os.path.join(directory_path, item)
            file_size = os.path.getsize(path)
            is_dir = os.path.isdir(path)
            files_info.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")

        return "\n".join(files_info)
    
    except Exception as e:
        return f'Error: listing files: {e}'
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)