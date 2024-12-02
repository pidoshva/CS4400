import subprocess

# Path to the code you want to analyze
path_to_code = "C:\\Users\\judit\\Desktop\\CS4400\\my_project"

# Run cloc via subprocess
result = subprocess.run(["cloc", path_to_code], capture_output=True, text=True)

# Print the result
print("Lines of Code Report:")
print(result.stdout)

