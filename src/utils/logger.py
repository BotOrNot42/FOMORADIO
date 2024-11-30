"""
Custom logger module for the framework
"""
import logging
from datetime import datetime
import os
from src.utils import dir_checker

# User Defined Variables
LOG_DIRECTORY = "logs"
FORMATTER = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")


def custom_logger(app_name) -> logging.Logger:
    """
    Custom Logger which creates the file based logging based on the
    App Name
    :param app_name: App's name
    :return: Basic Logger
    """
    c_logger = logging.getLogger(app_name)
    c_logger.setLevel(logging.DEBUG)
    current_date = datetime.now().strftime("%Y-%m-%d")
    log_filename = f"{app_name.replace(' ', '')}-{current_date}.log"
    # Ensure the log directory exists
    dir_checker(LOG_DIRECTORY)
    log_filepath = os.path.join(LOG_DIRECTORY, log_filename)
    # File Handler
    file_handler = logging.FileHandler(log_filepath)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(FORMATTER)
    c_logger.addHandler(file_handler)
    return c_logger
