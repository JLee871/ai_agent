import os

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
    
