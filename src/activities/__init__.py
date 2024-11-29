"""
Activities for the Fomo are handled here
"""
import time
from logging import Logger


def wait_for_next_show(seconds: int, logger: Logger):
    logger.info("Waiting for the next show to start. Stay Tuned!!!")
    time.sleep(seconds)
    logger.info("Wait is over. Lets Start!!!")
