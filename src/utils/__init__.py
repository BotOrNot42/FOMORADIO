"""
Utility Functions for Fomo
"""
import json
import os


def json_loader(path: str):
    """
    Utility Function to load json files as dictionary
    :param path: Path of the JSON File
    :return: JSON loaded as a dictionary
    """
    with open(path, "r", encoding="utf-8") as file:
        print(f"Loaded Configuration : {path}")
        return json.load(file)


def dir_checker(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as e:
            raise OSError(f"Error creating log directory: {e}") from e


def save_file(buffer, path: str):
    try:
        with open(path, "wb") as f:
            for chunk in buffer:
                f.write(chunk)
        return True, None
    except Exception as e:
        return False, str(e)
