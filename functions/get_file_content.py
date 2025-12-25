import os

from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))
        
        # Check if the target file is within the permitted working directory
        valid_file_path = os.path.commonpath([working_dir_abs, target_file_abs]) == working_dir_abs
        if not valid_file_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Check if the target file is actually a file
        if not os.path.isfile(target_file_abs):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Read the file and return its contents as a string
        ("Result for get_file_content('calculator', 'pkg/calculator.py')")
        content = f"Result for '{file_path}':"
        with open(target_file_abs, 'r') as f:
            print(f"MAX_CHARS is {MAX_CHARS}")
            content += f.read(MAX_CHARS)

            # After reading the first MAX_CHARS...
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

            return content
    except Exception as e:
        return f'Error: {e}'