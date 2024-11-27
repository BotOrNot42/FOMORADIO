"""
Base Class for all the data collectors
"""
from .granule import Granule


class BaseCollector:
    """
    Generic Collector
    """
    target_source: str = None

    def __init__(self):
        self.init()

    @property
    def source(self):
        return self.target_source

    def init(self):
        raise NotImplementedError


