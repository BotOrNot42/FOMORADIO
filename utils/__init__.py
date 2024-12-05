"""
Utility Functions for Fomo
"""
from typing import Tuple, Union
import json
import os
from .eexceptions import FomoException


def json_loader(path: str):
    """
    Utility Function to load json files as dictionary
    :param path: Path of the JSON File
    :return: JSON loaded as a dictionary
    """
    with open(path, "r", encoding="utf-8") as file:
        print(f"Loaded Configuration : {path}")
        return json.load(file)


def dir_checker(path) -> None:
    """
    Checks if the directory is existing or not. If the directory not exists
    this function will create one.
    :param path: Path of the directory to check
    :return: None
    """
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as exception:
            raise OSError(f"Error creating log directory: {exception}") from exception


def save_file(buffer, path: str) -> Tuple[bool, Union[None, str]]:
    """
    Saves a file in the given path provided the buffers
    :param buffer: Buffer of the file to be saved
    :param path: Path of the file to be saved
    :return: Bool if the file is saved or not along with the corresponding errors
    """
    try:
        with open(path, "wb") as file:
            for chunk in buffer:
                file.write(chunk)
        return True, None
    except FomoException as exception:
        return False, str(exception)
