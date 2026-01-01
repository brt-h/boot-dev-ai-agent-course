import os
import subprocess

from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file with optional command-line arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of command-line arguments to pass to the Python file",
            ),
        },
        required=["file_path"],
    ),
)

def run_python_file(working_directory, file_path, args=None):

    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Check if the target file is within the permitted working directory
        valid_file_path = os.path.commonpath([working_dir_abs, target_file_abs]) == working_dir_abs
        if not valid_file_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Check if the target file is actually a file
        if not os.path.isfile(target_file_abs):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        # Check if the target file is actually a python script
        if file_path[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'


        # Run python file as a subprocess
        command = ["python", target_file_abs]
        if args:
            command.extend(args)
        process = subprocess.run(command,capture_output=True, timeout=30 ,text=True)

        # Capture information related to the subprocess
        capture = ""
        if process.returncode != 0:
            capture += f"Process exited with code {process.returncode}"
        if (process.stdout == None) and (process.stderr == None):
            capture += "No output produced"
        else:
            capture += f"STDOUT: {process.stdout}"
            capture += f"STDERR: {process.stderr}"
        return capture

    except Exception as e:
        return f"Error: executing Python file: {e}"
