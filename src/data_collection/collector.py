"""
Base Class for all the data collectors
"""
from .granule import Granule


class BaseCollector:
    """
    Generic Collector
    """
    source: str = None

    def __init__(self):
        pass

    def fetch(self):
        raise NotImplementedError

    def process(self):
        records, timestamp_key, content_key = self.fetch()
        granular_records = []
        for each_record in records:
            timestamp = each_record[timestamp_key]
            content = each_record[content_key]
            del each_record[timestamp_key]
            del each_record[content_key]
            granular_records.append(Granule(self.source, timestamp, content, each_record))
        return [i.to_dict() for i in granular_records]
