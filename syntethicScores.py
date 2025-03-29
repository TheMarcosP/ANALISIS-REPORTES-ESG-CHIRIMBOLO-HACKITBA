import sys
import os
import numpy as np

# List files in a directory path
def list_files_in_directory(path):
    """
    List all files in a directory.

    Args:
        path (str): The directory path.

    Returns:
        list: A list of file names in the directory.
    """
    try:
        return sorted(os.listdir(path))
    except FileNotFoundError:
        print(f"Directory {path} not found.")
        return []
    except PermissionError:
        print(f"Permission denied to access {path}.")
        return []
    


# Count the number of entries of a json file
import json

def count_json_entries(file_path):
    """
    Count the number of entries in a JSON file.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        int: The number of entries in the JSON file.
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            return len(data)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return 0
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {file_path}.")
        return 0
    
path = "data/scores.json"
files = count_json_entries(path)
print(f"Number of entries in {path}: {files}")





# Check if the name of each file has a key in the json file
def check_json_keys_in_files(json_file, directory):
    """
    Check if the names of files in a directory are keys in a JSON file.

    Args:
        json_file (str): The path to the JSON file.
        directory (str): The directory path.

    Returns:
        list: A list of file names that are not keys in the JSON file.
    """
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
            json_keys = set(data.keys())
    except FileNotFoundError:
        print(f"File {json_file} not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {json_file}.")
        return []

    files = list_files_in_directory(directory)
    missing_files = [file for file in files if file not in json_keys]
    return missing_files

path = "data/scores.json"
directory = "data/reports"
missing_files = check_json_keys_in_files(path, directory)
print(f"Missing files in {directory} that are not keys in {path}:")
for file in missing_files:
    print(file)
