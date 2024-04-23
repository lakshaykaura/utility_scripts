import os
import re
from pathlib import Path


def get_subfolders_in_ruleflowgroup_order(path):
    """
    Retrieves and sorts the subfolders in a given directory.

    Args:
        path (str): The path to the directory.

    Returns:
        list: A list of subfolder names, sorted based on a custom rule.

    This function lists all items in the specified directory and filters out any that are not directories.
    It then sorts the directories based on a custom rule: directories starting with 'L' followed by a number
    are sorted based on this number. If there is a secondary number (like the "7" in "L155_7"), it is used for
    secondary sorting. Directories that do not match this pattern are placed at the end of the list.
    """
    # Extract the folders
    folders_only = [
        item for item in os.listdir(path) if os.path.isdir(os.path.join(path, item))
    ]

    # Custom sorting function
    def custom_sort(item):
        # Try to extract a number from the name after 'L'
        match = re.match(r"L(\d+)(?:_(\d+))?", item)
        if match:
            main_num = int(match.group(1))
            # If there's a secondary number (like the "7" in "L155_7"), use it, otherwise default to 0
            sub_num = int(match.group(2)) if match.group(2) else 0
            return (main_num, sub_num)
        # For other items, place them at the end
        return (float("inf"), 0)

    return sorted(folders_only, key=custom_sort)


def compare_directories(dir1: Path, dir2: Path):
    """
    Compares the contents of two directories.

    Args:
        dir1 (Path): The first directory to compare.
        dir2 (Path): The second directory to compare.

    Returns:
        tuple: A tuple containing two sets. The first set contains the files that are only in dir1.
               The second set contains the files that are only in dir2.

    This function walks through each directory and its subdirectories, adding each file to a set.
    The file paths are stored as relative paths from the root of their respective directories.
    The function then calculates the intersection of the two sets (the files that are in both directories)
    and subtracts this from each set to get the files that are only in one directory or the other.
    """
    dir1_files = set()
    dir2_files = set()

    for root, _, files in os.walk(dir1):
        for file in files:
            dir1_files.add(Path(root, file).relative_to(dir1))

    for root, _, files in os.walk(dir2):
        for file in files:
            dir2_files.add(Path(root, file).relative_to(dir2))

    common = dir1_files.intersection(dir2_files)
    only_in_dir1 = dir1_files - common
    only_in_dir2 = dir2_files - common

    return only_in_dir1, only_in_dir2
