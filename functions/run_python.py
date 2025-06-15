import os, subprocess

def run_python_file(working_directory, file_path, args=None):
    if file_path[-3:] != '.py':
        return f'Error: "{file_path}" is not a Python file.'

    working_path = os.path.abspath(working_directory)
    file_abs_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not file_abs_path.startswith(working_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(file_abs_path):
        return f'Error: File "{file_path}" not found.'
    
    try:
        commands = ["python3", file_abs_path]
        if args:
            commands.extend(args)
        completed_process = subprocess.run(commands, capture_output=True, text=True, timeout=30, cwd=working_path)

        if not completed_process.stdout and not completed_process.stderr:
            return "No output produced."
        
        output = []
        if completed_process.stdout:
            output.append(f'STDOUT:\n{completed_process.stdout}')
        if completed_process.stderr:
            output.append(f'STDERR:\n{completed_process.stderr}')
        if completed_process.returncode != 0:
            output.append(f'Process exited with code {completed_process.returncode}')
        
        if not output:
            return "No output produced."
        
        return "\n".join(output)
        
    
    except Exception as e:
        return f'Error: executing Python file: {e}'