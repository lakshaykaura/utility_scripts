import utils.files as file_utils

# Get user input
path_to_directory = input("Please enter the directory path: ")

# Handle backslashes and spaces
path_to_directory = path_to_directory.strip()  # Remove any leading/trailing spaces
path_to_directory = path_to_directory.replace(
    "\\", "\\\\"
)  # Replace single backslashes with double backslashes

# Print each directory on a new line
for folder in file_utils.get_subfolders_in_ruleflowgroup_order(path_to_directory):
    print(folder)
