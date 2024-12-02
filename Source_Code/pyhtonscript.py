from pycloc import CLOC

# Specify the path to the project or file
path_to_code = "path/to/your/code"

# Run pycloc to count lines of code
result = CLOC.run(path=path_to_code)

# Print the result
print("Lines of Code Report:")
print(result)
