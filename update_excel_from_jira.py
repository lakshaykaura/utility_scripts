"""
Script Name: script_to_update_excel_from_jira.py
Description:   
    This script is a comprehensive tool designed to automate the tracking and updating of JIRA issue details within an Excel workbook. 
    It utilizes several Python modules to perform a variety of tasks, including manipulating Excel files, interacting with web pages through Selenium, and enhancing logging and output presentation.
    Below is a detailed breakdown of its components and functionalities.

Script Overview:   
    Purpose: Automates the synchronization of JIRA issue details with an Excel-based defect tracker.
    Key Technologies: Python, Selenium WebDriver for browser automation, xlwings for Excel manipulation, and Rich for enhanced console output and logging.

Dependencies:
    External Modules:
        selenium: For automating web browser interaction.
        xlwings: To manipulate Microsoft Excel files.
        pandas: For data manipulation and analysis.
        rich: To enrich logging and console output with colors and progress bars.
        webdriver_manager: To manage the browser driver automatically.
    Python Standard Libraries:
        logging: For logging messages.
        os: To interact with the operating system, like fetching environment variables.
        shutil: For high-level file operations.
        datetime: To work with dates and times.

Functions and Their Functionalities:
Utility Functions:
    get_sentence_case: Converts strings to sentence case.
    is_date: Checks if a given value is a date.
    format_date: Formats date strings.
    parse_date: Parses date strings into datetime objects.
    are_dates_equal: Compares two dates, ignoring time components.
    modify_assignee: Modifies assignee names to a standard format.
    check_if_value_is_updated: Checks if a cell value in Excel needs to be updated.

Excel Manipulation Functions:
    get_column_letter_from_index: Converts column index to Excel column letters.
    get_column_letter_by_header: Maps column headers to their corresponding letter representations.
    get_jira_ids_from_excel_sheet: Extracts JIRA IDs from an Excel sheet.

JIRA Interaction Functions:
    login_to_jira: Automates login to JIRA.
    navigate_to_jira_issue_filter_page: Navigates to a specific JIRA issue filter page.
    wait_for_jira_resultset_to_refresh: Waits for JIRA's issue result set to refresh.
    update_jql_query_with_jira_ids: Updates the JQL query to include specific JIRA IDs.
    get_property_from_issue_html: Extracts issue details from HTML.
    fetch_and_add_issue_details_in_dataframe: Fetches issue details and adds them to a dataframe.
    extract_issue_details_from_jira: Extracts issue details from JIRA.

Script Flow:
    Initialization: Sets up logging, constants, and configurations.
    Backup Excel File: Creates a backup of the Excel defect tracker before making changes.
    Open Excel Workbook: Uses xlwings to open and interact with the Excel file.
    Read Data from Excel: Extracts necessary data from the Excel workbook to identify which JIRA issues to update.
    Setup Selenium WebDriver: Configures and initializes the Chrome WebDriver.
    Login to JIRA: Logs into the JIRA web interface using credentials.
    Navigate and Query JIRA: Accesses the JIRA issue filter page and updates the JQL query to target specific issues.
    Extract and Process JIRA Issue Details: Fetches details for each targeted issue and processes them.
    Update Excel Workbook: Applies extracted data to the Excel workbook, updating issue details and tracking changes.
    Finalization: Saves changes to the Excel workbook, handles exceptions, and restores the original file in case of errors.

Exception Handling and Logging:
    The script employs try-except blocks to manage exceptions gracefully, ensuring any errors are logged and, if necessary, the original Excel file is restored from backup.
    Rich library is used to enhance logging with color-coded messages and to provide a visually appealing progress bar for tracking operations.

Execution and Error Management:
    The script includes comprehensive error handling and logging, with specific attention to potential issues that may arise during the automation process.
    A final block ensures that the Excel application is properly closed, changes are saved, and resources are freed, even in the event of an error.

This script exemplifies a sophisticated automation task that bridges the gap between project management tools (JIRA) and local project tracking (Excel), enhancing productivity and accuracy in tracking defects.
Author: Kaura, Lakshay
Created: 2024-03-21
Last Updated: 2024-03-21
"""

import logging
import os
import shutil
import pandas as pd
import xlwings.constants as xlconst
from rich.console import Console
from rich.logging import RichHandler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import utils.common as common_utils
import utils.excel as excel_utils
import utils.jira as jira_utils
import utils.progress as progress_utils

console = Console()

timeout_in_sec = 30

logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, console=console)],
)

logging.getLogger("webdriver_manager").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("WDM").setLevel(logging.ERROR)

logger = logging.getLogger("rich")

exception_occurred = False

# Use rich's console for printing messages
console.print("[green]🚀 Starting script execution...[/green]")

# Path to your Excel file
excel_file = r"C:\Users\lkaura\Downloads\Daily_Defect_Tracker.xlsx"

backup_file = excel_utils.backup_excel_file(excel_file)
console.print("[yellow]Backup of the Excel file created successfully.[/yellow]")

app = None
wb = None

try:

    app, wb = excel_utils.open_workbook(excel_file, visible=False)
    console.print("[blue]Excel workbook opened and 'Defects' sheet selected.[/blue]")

    sheet = wb.sheets["Defects"]

    for table in sheet.api.ListObjects:
        table.AutoFilter.ShowAllData()

    header_row = 1

    row_start = 2

    last_row = sheet.range("A" + str(sheet.cells.last_cell.row)).end("up").row

    last_col = sheet.range("XFD" + str(header_row)).end("left").column

    column_map = excel_utils.get_column_letter_by_header(sheet, header_row, last_col)

    updates_column = column_map["Jira Updates"]
    sheet.range(f"{updates_column}2:{updates_column}{last_row}").value = [[""]]
    console.print("[magenta]Cleared 'Jira Updates' column in Excel.[/magenta]")

    jira_id_to_row_map = excel_utils.get_jira_ids_from_excel_sheet(
        sheet, last_row, column_map
    )
    console.print("[green]Jira Ids read successfully from Excel sheet.[/green]")

    chrome_options = Options()
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )

    console.print("[cyan]Logging into Jira...[/cyan]")
    jira_utils.login_to_jira(driver, timeout_in_sec)
    console.print("[cyan]Successfully Logged into Jira.[/cyan]")

    console.print("[magenta]Navigating to Jira issue filter page...[/magenta]")
    jira_utils.navigate_to_jira_issue_filter_page(driver, timeout_in_sec)
    console.print(
        "[magenta]Successfully navigated to Jira issue filter page.[/magenta]"
    )

    console.print("[yellow]Capturing Jira IDs and comparing with excel...[/yellow]")
    jira_utils.update_jql_query_with_jira_ids(driver, jira_id_to_row_map)
    console.print("[blue]JQL query updated with Jira IDs.[/blue]")

    issues, exception_occurred = jira_utils.extract_issue_details_from_jira(
        driver, timeout_in_sec
    )
    console.print("[magenta]Issue details extracted from Jira.[/magenta]")

    data = []

    processed_jira_ids = set()

    if not exception_occurred:
        progress = progress_utils.create_progress_bar(console)
        progress.start()
        task1 = progress.add_task("[cyan]Processing issues...", total=len(issues))
        for issue in issues:
            if exception_occurred:
                break
            issue_details, exception_occurred = (
                jira_utils.fetch_and_add_issue_details_in_dataframe(issue)
            )
            if (
                issue_details is not None
                and issue_details[jira_utils.JIRA_ID]
                and issue_details[jira_utils.JIRA_ID] not in processed_jira_ids
            ):
                data.append(issue_details)
                processed_jira_ids.add(issue_details[jira_utils.JIRA_ID])
            progress.update(task1, advance=1)
        console.print("[cyan]Issues processed, updating Excel...[/cyan]")
        driver.quit()

        df_issues = pd.DataFrame(data)
        if not exception_occurred:
            task2 = progress.add_task(
                "[magenta]Updating Excel...", total=len(df_issues)
            )
            for index, row in df_issues.iterrows():
                jira_id = row[jira_utils.JIRA_ID]
                excel_row = jira_id_to_row_map.get(jira_id)
                if excel_row:
                    # Flag to track if any update is made
                    is_updated = False
                    changes = set()
                    for key, value in row.items():
                        if key in column_map:
                            col_letter = column_map[key]
                            current_value = sheet.range(
                                f"{col_letter}{excel_row}"
                            ).value
                            if common_utils.check_if_value_is_updated(
                                value, current_value
                            ):
                                sheet.range(f"{col_letter}{excel_row}").value = value
                                changes.add(key)
                                is_updated = True

                    if is_updated:
                        existing_history = (
                            sheet.range(f"{updates_column}{excel_row}").value or ""
                        )
                        existing_changes = (
                            set(existing_history.split(" | "))
                            if existing_history
                            else set()
                        )
                        new_changes = existing_changes.union(changes)
                        new_history_value = "Updates : " + " | ".join(new_changes)
                        sheet.range(f"{updates_column}{excel_row}").value = (
                            new_history_value
                        )

                else:
                    # If Jira ID not found, find the last non-empty row in the Jira ID column and append new issue data
                    last_non_empty_row = (
                        sheet.range("A" + str(sheet.cells.last_cell.row)).end("up").row
                    )
                    next_empty_row = last_non_empty_row + 1

                    for key, value in row.items():
                        if key in column_map:
                            col_letter = column_map[key]
                            sheet.range(f"{col_letter}{next_empty_row}").value = value

                    # Mark the row as "New"
                    sheet.range(f"{updates_column}{next_empty_row}").value = "New"

                    # Update the jira_id_to_row_map to include this new Jira ID with its corresponding row
                    jira_id_to_row_map[jira_id] = next_empty_row
                progress.update(task2, advance=1)
            console.print("[yellow]Excel updated with issue details.[/yellow]")

            progress.stop()
            # Align all content in center-left.
            used_range = sheet.used_range
            used_range.api.HorizontalAlignment = xlconst.HAlign.xlHAlignLeft
            used_range.api.VerticalAlignment = xlconst.VAlign.xlVAlignCenter

            if not exception_occurred:
                console.print(
                    "[green]✨ Script execution completed successfully 🚀[/green]",
                    style="green",
                )
            else:
                console.print(
                    "[red]Script execution terminated due to an error. Please check the logs for more details.[/red] ❌"
                )

except Exception as e:
    exception_occurred = True
    console.print(f"[red]An error occurred:{e}[/red] ❌")

finally:
    console.print("[cyan]Finalizing changes and closing Excel workbook...[/cyan]")
    # personal_wb.close()
    if wb is not None:
        wb.save(excel_file)
        wb.close()
    if app:
        app.quit()
    if exception_occurred:
        console.print(
            "[yellow]An exception occurred. Restoring the original Excel file from backup...[/yellow]"
        )
        try:
            if os.path.exists(excel_file):
                os.remove(excel_file)
            shutil.move(backup_file, excel_file)
            console.print(
                "[green]The original Excel file has been restored successfully.[/green]"
            )
        except Exception as e:
            console.print(
                f"[red]Failed to restore the original Excel file. Error: {e}[/red]"
            )
