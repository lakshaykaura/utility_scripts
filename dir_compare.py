import sys
import argparse
from pathlib import Path
import utils.files as file_utils

parser = argparse.ArgumentParser(
    description="Compare two directories and list differences."
)
print("Compare two directories and list differences.")
dir1 = input("Please enter the path to the first directory: ")
dir2 = input("Please enter the path to the second directory: ")

dir1 = Path(dir1)
dir2 = Path(dir2)

if not dir1.is_dir() or not dir2.is_dir():
    print("Both arguments must be valid directories.")
    sys.exit(1)

only_in_dir1, only_in_dir2 = file_utils.compare_directories(dir1, dir2)

if only_in_dir1:
    print(f"Files and directories only in {dir1}:")
    for item in sorted(only_in_dir1):
        print(f"  {item}")

if only_in_dir2:
    print(f"Files and directories only in {dir2}:")
    for item in sorted(only_in_dir2):
        print(f"  {item}")

if not only_in_dir1 and not only_in_dir2:
    print("Both directories are identical.")
