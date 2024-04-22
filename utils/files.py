import os
import re
from pathlib import Path


def get_subfolders(path):
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
