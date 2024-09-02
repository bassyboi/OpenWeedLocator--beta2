import json
import os

def apply_changes(changes_file):
    with open(changes_file, 'r') as file:
        changes = json.load(file)

    for change in changes:
        file_path = change['file']
        line_number = change['line']
        new_code = change['new_code']

        # Read the file
        with open(file_path, 'r') as f:
            lines = f.readlines()

        # Apply the change
        lines[line_number - 1] = new_code + '\n'

        # Write back to the file
        with open(file_path, 'w') as f:
            f.writelines(lines)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python apply_changes.py <changes_file.json>")
        exit(1)
    apply_changes(sys.argv[1])
