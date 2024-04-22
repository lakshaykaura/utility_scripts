import utils.excel as excel_utils

# Ask the user for the directory path
directory_path = input("Please enter the directory path: ")

# Specify the macro name
macro_name = (
    "AddOrUpdateRuleFlowGroupAsPerPath"  # Change if your macro name is different
)

excel_utils.run_vba_macro_on_files_in_directory(directory_path, macro_name)
