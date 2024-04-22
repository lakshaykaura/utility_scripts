import os
import xlwings as xw
import shutil
import win32com.client
import openpyxl
import xlrd


def run_vba_macro_on_files_in_directory(directory_path, macro_name):
    # Create an Excel application object
    excel_app = win32com.client.Dispatch("Excel.Application")
    excel_app.Visible = False  # We keep Excel in the background

    # Ensure PERSONAL.XLSB is open to access the macro
    try:
        personal_wb = excel_app.Workbooks("PERSONAL.XLSB")
    except:
        personal_wb = excel_app.Workbooks.Open(
            excel_app.StartupPath + r"\PERSONAL.XLSB"
        )

    # Loop through all files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".xls") or filename.endswith(".xlsx"):
            file_path = os.path.join(directory_path, filename)

            # Open the workbook
            wb = excel_app.Workbooks.Open(file_path)

            # Run the macro
            excel_app.Run(macro_name)

            # Close the workbook
            wb.Close(SaveChanges=True)

    # Quit the Excel application
    excel_app.Quit()


def backup_excel_file(file_path):
    """
    Creates a backup of the Excel file.

    Args:
        file_path (str): The full path to the Excel file to be backed up.

    Returns:
        str: The file path of the backed-up Excel file.
    """
    backup_file_path = file_path.replace(".xlsx", "_backup.xlsx")
    shutil.copy(file_path, backup_file_path)
    return backup_file_path


def open_workbook(file_path, visible=False):
    """
    Opens an Excel workbook.

    Args:
        file_path (str): The full path to the Excel file to be opened.
        visible (bool): Specifies whether the Excel application should be visible.

    Returns:
        tuple: A tuple containing the Excel app and workbook instances.
    """
    app = xw.App(visible=visible)
    wb = app.books.open(file_path)
    return app, wb


def get_column_letter_from_index(index):
    """
    Converts a 1-based column index into its corresponding Excel column letter.

    Excel columns are labeled alphabetically starting with 'A' for the first column, 'B' for the second, and so on,
    up to 'Z' for the 26th column. After 'Z', columns continue with double letters starting from 'AA', 'AB', etc.
    This function calculates the corresponding Excel column letter for a given 1-based column index.

    Parameters:
    - index (int): The 1-based index of the column. The first column has an index of 1, not 0.

    Returns:
    - str: The Excel column letter corresponding to the provided index.

    Raises:
    - ValueError: If the provided index is less than 1 since Excel columns are 1-based.

    Note: This function is designed to work with indices that represent valid Excel column positions. Excel supports
    up to 16,384 columns as of Excel 2019 and Office 365, corresponding to column 'XFD'.
    """
    if index < 1:
        raise ValueError("Index is too small")
    result = ""
    while index > 0:
        index, remainder = divmod(index - 1, 26)
        result = chr(65 + remainder) + result
    return result


def get_column_letter_by_header(sheet, header_row, last_col):
    """
    Creates a dictionary mapping header names to column letters in the specified header row.

    :param sheet: The xlwings Sheet object.
    :param header_row: The row number of the header row.
    :return: A dictionary mapping header names to column letters.
    """
    headers = sheet.range(f"{header_row}:{header_row}").value[:last_col]
    return {
        header: get_column_letter_from_index(index + 1)
        for index, header in enumerate(headers)
        if header is not None
    }


def get_jira_ids_from_excel_sheet(sheet, last_row, column_map):
    status_column = column_map["Status"]
    jira_id_to_row_map = {}

    for row in range(2, last_row + 1):
        jira_id_cell = f"A{row}"
        status_cell = f"{status_column}{row}" if status_column else None

        jira_id = sheet.range(jira_id_cell).value
        status = sheet.range(status_cell).value if status_cell else None

        if jira_id and status != "Done":
            jira_id_to_row_map[jira_id] = row

    return jira_id_to_row_map


def search_xlsx(file_name, keyword):
    workbook = openpyxl.load_workbook(file_name)
    for sheet in workbook:
        for row in sheet.iter_rows():
            for cell in row:
                if cell.value and keyword in str(cell.value):
                    return True
    return False


def search_xls(file_name, keyword):
    workbook = xlrd.open_workbook(file_name)
    for sheet in workbook.sheets():
        for row in range(sheet.nrows):
            for col in range(sheet.ncols):
                cell = sheet.cell(row, col)
                if cell.value and keyword in str(cell.value):
                    return True
    return False


def search_for_keyword_in_excel_files_within_directory(directory, keyword):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith((".xls", ".xlsx")):
                file_path = os.path.join(root, file)
                print(f"\nChecking file {file_path} for keyword {keyword}...\n")
                if file.endswith(".xlsx"):
                    found = search_xlsx(file_path, keyword)
                else:
                    found = search_xls(file_path, keyword)
                if found:
                    os.startfile(file_path)
