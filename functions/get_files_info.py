import os

from google.genai import types

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

def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir_abs = os.path.normpath(os.path.join(working_dir_abs, directory))
        
        # Check if the target directory is within the permitted working directory
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir_abs]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Check if the target directory is actually a directory
        if not os.path.isdir(target_dir_abs):
            return f'Error: {directory} is not a directory'

        # desired return format in happy path:
        # - README.md: file_size=1032 bytes, is_dir=False
        # - src: file_size=128 bytes, is_dir=True
        # - package.json: file_size=1234 bytes, is_dir=False

        # Iterate over items in the target directory and assemble the return object including
        # (for all items) the name, file size, and whether its a directory itself

        info = f"Result for '{directory}':"
        for item in os.listdir(target_dir_abs):
            item_name = item
            item_path = os.path.join(target_dir_abs, item)
            item_size = os.path.getsize(item_path)
            item_is_dir = os.path.isdir(item_path)
            info += f'\n- {item_name}: file_size={item_size} bytes, is_dir={item_is_dir}'
        return info
    except Exception as e:
        return f'Error: {e}'