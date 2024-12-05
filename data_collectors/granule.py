"""
Base Class to handle the data from multiple sources
"""

import json
from dateutil.parser import parse


class Granule:
    """
    Granule represents the smallest basic particle of data collection
    Data can be from any source but has to be converted to Granule to
    pass on to the next function
    """

    def __init__(self, source, timestamp, content, user, metadata=None):
        """
        Initialize a new DataEntry object.

        :param source: The source of the data (e.g., "twitter", "telegram").
        :param timestamp: The timestamp of the data (e.g., ISO 8601 string).
        :param content: The actual content (e.g., tweet text, message text).
        :param user: The author of the content (e.g., 123, Degen).
        :param metadata: A dictionary containing additional metadata (optional).
        """
        self.source = source
        self.timestamp = parse(timestamp)
        self.content = content
        self.user = user
        self.metadata = metadata if metadata else {}

    def to_dict(self):
        """
        Convert the DataEntry object to a dictionary.

        :return: A dictionary representation of the DataEntry.
        """
        return {
            "source": self.source,
            "timestamp": str(self.timestamp),
            "content": self.content,
            "user": self.user,
            "metadata": self.metadata,
        }

    def to_json(self):
        """
        Convert the DataEntry object to a JSON string.

        :return: A JSON string representation of the DataEntry.
        """
        return json.dumps(self.to_dict(), indent=4)

    @classmethod
    def from_dict(cls, data_dict):
        """
        Create a DataEntry object from a dictionary.

        :param data_dict: A dictionary containing the data (matching the structure).
        :return: A DataEntry object.
        """
        return cls(
            source=data_dict.get("source"),
            timestamp=parse(data_dict.get("timestamp")),
            content=data_dict.get("content"),
            user=data_dict.get("user"),
            metadata=data_dict.get("metadata", {}),
        )

    @classmethod
    def from_json(cls, json_data):
        """
        Create a DataEntry object from a JSON string.

        :param json_data: A JSON string containing the data.
        :return: A DataEntry object.
        """
        data_dict = json.loads(json_data)
        return cls.from_dict(data_dict)

    def __repr__(self):
        """Return a string representation of the object."""
        return (
            f"DataEntry(source={self.source}, timestamp={str(self.timestamp)}, "
            f"content={self.content}, user={self.user}, metadata={self.metadata})"
        )
