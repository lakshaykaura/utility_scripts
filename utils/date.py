from datetime import datetime

import pandas as pd


def is_date(value):
    """
    Determines whether the given value is a date object.

    This function checks if the passed value is an instance of `datetime.datetime` or `pandas.Timestamp`, effectively identifying if it represents a date.

    Parameters:
    - value (any): The value to be checked. This can be of any type but typically expected to be either a `datetime.datetime` object, a `pandas.Timestamp`, or similar date/time representations.

    Returns:
    - bool: True if the value is an instance of `datetime.datetime` or `pandas.Timestamp`, False otherwise.
    """
    return isinstance(value, (datetime, pd.Timestamp))


def format_date(date_str):
    """
    Formats a date string from ISO 8601 format to 'dd-mm-yyyy' format.

    This function attempts to parse a date string expected to be in the ISO 8601 format ('YYYY-MM-DDTHH:MM:SS+timezone'), and if successful, converts it to a more readable 'dd-mm-yyyy' format. If the input string is not a valid date or is empty, the function returns an empty string. If the date string is in an incorrect format and cannot be parsed, the original date string is returned.

    Parameters:
    - date_str (str): The date string to be formatted, expected to be in the ISO 8601 format.

    Returns:
    - str: The formatted date string in 'dd-mm-yyyy' format if parsing is successful; otherwise, returns the original string or an empty string if the input is null or empty.
    """
    if pd.isnull(date_str) or date_str == "":
        return ""
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S%z")
    except ValueError:
        return date_str
    # Formatting to 'dd-mm-yyyy'
    return date_obj.strftime("%d-%m-%Y")


def parse_date(date_str):
    """
    Parses a date string in ISO 8601 format and returns a datetime object.

    This function attempts to convert a date string in the ISO 8601 format ('YYYY-MM-DDTHH:MM:SS+timezone') into a `datetime.datetime` object. If the input string is null, empty, or if the date string does not match the expected format, the function returns None.

    Parameters:
    - date_str (str): The date string to be parsed, expected to be in the ISO 8601 format.

    Returns:
    - datetime.datetime or None: A `datetime.datetime` object representing the date if parsing is successful; None if the input is null, empty, or the date string is not in the correct format.
    """
    if pd.isnull(date_str) or date_str == "":
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S%z")
    except ValueError:
        return None


def are_dates_equal(excel_date, python_date):
    """
    Compares the date part of an Excel datetime with a Python datetime or Timestamp object, ignoring time and timezone.

    This function checks whether the date part (year, month, day) of two datetime objects are equal, disregarding any time or timezone information. It's useful for comparing dates when the time component is not relevant. The function handles `datetime.datetime` and `pandas.Timestamp` objects, converting the latter to `datetime.datetime` for comparison.

    Parameters:
    - excel_date (datetime.datetime): The date from Excel, expected to be a `datetime.datetime` object.
    - python_date (datetime.datetime or pandas.Timestamp): The date to compare with, which can be either a `datetime.datetime` object or a `pandas.Timestamp`.

    Returns:
    - bool: True if the dates are equal, False otherwise. Returns False immediately if either date is null.
    """
    # Check if either value is None, which indicates missing data
    if pd.isnull(excel_date) or pd.isnull(python_date):
        return False

    # Ensure python_date is a datetime object for comparison
    if isinstance(python_date, pd.Timestamp):
        python_date = python_date.to_pydatetime()

    # Compare only the date components
    return excel_date.date() == python_date.date()
