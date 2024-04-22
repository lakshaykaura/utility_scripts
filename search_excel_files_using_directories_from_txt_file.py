import utils.excel as excel_utils

directory_file = input("Please enter the path to the directory file: ")
keyword = input("Please enter the keyword: ")

with open(directory_file, "r") as f:
    directories = f.readlines()

for directory in directories:
    excel_utils.search_for_keyword_in_excel_files_within_directory(
        directory.strip(), keyword
    )
