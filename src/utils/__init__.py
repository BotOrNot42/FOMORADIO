"""
Utility Functions for Fomo
"""
import json


def json_loader(path: str):
    """
    Utility Function to load json files as dictionary
    :param path: Path of the JSON File
    :return: JSON loaded as a dictionary
    """
    with open(path, "r", encoding="utf-8") as file:
        print(f"Loaded Configuration : {path}")
        return json.load(file)
