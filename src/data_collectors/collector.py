"""
Base Class for all the data collectors
"""
from typing import Tuple, List, Dict
from .granule import Granule


class BaseCollector:
    """
    Generic Collector
    """
    source: str = None

    def __init__(self):
        """
        Will be overridden in the child classes
        """

    def fetch(self) -> Tuple[List[Dict], str, str]:
        """
        Will be overridden in the child classes
        """
        raise NotImplementedError

    def process(self) -> List[Dict]:
        """
        Wrapper method for different fetching methods which
        converts the data into Granule and passes it as a
        dictionary to the consumer classes.
        :return: List of Messages/Texts/Tweets
        """
        records, timestamp_key, content_key = self.fetch()
        granular_records = []
        for each_record in records:
            timestamp = each_record[timestamp_key]
            content = each_record[content_key]
            del each_record[timestamp_key]
            del each_record[content_key]
            granular_records.append(
                Granule(self.source, timestamp, content, each_record)
            )
        return [i.to_dict() for i in granular_records]
