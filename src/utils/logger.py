import logging
from datetime import datetime
import os

# Define the log directory and file name
log_directory = "."

# Ensure the log directory exists
if not os.path.exists(log_directory):
    try:
        os.makedirs(log_directory)
    except OSError as e:
        raise Exception(f"Error creating log directory: {e}")

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def custom_logger(app_name):
    c_logger = logging.getLogger(app_name)
    c_logger.setLevel(logging.DEBUG)

    # Log File Name
    log_filename = app_name + '-{:%Y-%m-%d}.log'.format(datetime.now())
    log_filepath = os.path.join(log_directory, log_filename)

    # Create a handler (FileHandler) with the log file path
    file_handler = logging.FileHandler(log_filepath)
    file_handler.setLevel(logging.DEBUG)

    # Set formatter for the handler
    file_handler.setFormatter(formatter)
    c_logger.addHandler(file_handler)
    return c_logger
