import os

from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites content to a file at the specified path",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)

def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))
        target_file_dir_abs = os.path.dirname(target_file_abs)

        # Check if the target file is within the permitted working directory
        valid_file_path = os.path.commonpath([working_dir_abs, target_file_abs]) == working_dir_abs
        if not valid_file_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # Check if the target file is actually a directory
        if os.path.isdir(target_file_abs):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(target_file_dir_abs, exist_ok=True)
        
        with open(target_file_abs, 'w') as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: {e}'
