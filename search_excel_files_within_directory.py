import sys
import os
import glob
import utils.files as file_utils
import utils.excel as excel_utils


directory = input("Please enter the path to the directory file: ")
keyword = input("Please enter the keyword: ")

matches = []

for file_type in ["*.xls", "*.xlsx"]:
    for file_name in glob.glob(os.path.join(directory, file_type)):
        if file_name.endswith(".xlsx"):
            found = excel_utils.search_xlsx(file_name, keyword)
        elif file_name.endswith(".xls"):
            found = excel_utils.search_xls(file_name, keyword)
        else:
            continue

        if found:
            matches.append(file_name)

if matches:
    for match in matches:
        print(f"\nMatch found in: {match}...\n")
        os.system(f'start excel "{match}"')
else:
    print(f"No matches found for keyword '{keyword}' in directory '{directory}'...\n")
