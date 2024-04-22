import sys
import utils.java as java_utils

try:
    file_path = (
        sys.argv[1] if len(sys.argv) > 1 else input("Enter the path to the Java file: ")
    )
    file_path = file_path.strip().replace("/", "\\")

    print(f"Reading file: {file_path}")

    with open(file_path, "r") as file:
        file_contents = file.read()

    print("File contents read successfully.")
    print("Starting parsing process...")

    call_hierarchy = java_utils.parse_java_code(file_contents)

    if not call_hierarchy:
        print("No method invocations found. Please check the Java file.")

    java_utils.detect_and_print_cycles(call_hierarchy)
    print(f"Call hierarchy: {call_hierarchy}")

    print("Cycle detection complete.")

except Exception as e:
    print(f"An error occurred: {e}")
