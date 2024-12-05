"""
Activities for the Fomo are handled here
"""
import time
from logging import Logger


def wait_for_next_show(seconds: int, logger: Logger) -> None:
    """
    Activity function to sit tight and wait for the next show
    :param seconds: Seconds to wait for the next show
    :param logger: Logger to make the viewers stay tuned
    :return: None
    """
    logger.info("Waiting for the next show to start. Stay Tuned!!!")
    time.sleep(seconds)
    logger.info("Wait is over. Lets Start!!!")
