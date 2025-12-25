from functions.get_file_content import get_file_content

print(get_file_content("calculator", "main.py"))

print(get_file_content("calculator", "pkg/calculator.py"))

print("This should return an error string:")
print(get_file_content("calculator", "/bin/cat"))

print("This should return an error string:")
print(get_file_content("calculator", "pkg/does_not_exist.py"))