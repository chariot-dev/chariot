import abc
from typing import List, Type, Dict

from chariot.database.DatabaseConfiguration import DatabaseConfiguration
from chariot.JSONTypes import JSONDict, JSONObject


class DatabaseWriter(metaclass=abc.ABCMeta):
    def __init__(self, databaseConfiguration: Type[DatabaseConfiguration]):
        self.databaseConfiguration: Type[DatabaseConfiguration] = databaseConfiguration
        self.connect()
        self.initializeTable()

    def __del__(self):
        pass

    @staticmethod
    def checkDataPoint(dataPoint: Dict[str, JSONObject]):
        """
        Check for validity of a dataPoint. dataPoint should have keys
        "relative_time" and "freeform". If dataPoint is missing either,
        or if it has extra keys, this function raises a ValueError.
        """
        if 'relative_time' not in dataPoint.keys():
            raise ValueError('Data point has no "relative_time" key')
        elif 'freeform' not in dataPoint.keys():
            raise ValueError('Data point has no "freeform" key')
        else:
            for key in dataPoint.keys():
                if key not in ["relative_time", "freeform"]:
                    raise ValueError('Data point has extraneous keys')

    @abc.abstractmethod
    def connect(self):
        """
        Establish a connection to the database.
        """
        pass

    @abc.abstractmethod
    def disconnect(self):
        """
        End connection to the database gracefully.
        """
        pass

    @abc.abstractmethod
    def initializeTable(self):
        """
        Create a table in the database.
        """
        pass

    @abc.abstractmethod
    def insertOne(self, dataPoint: Dict[str, JSONObject]):
        """
        Check for validity of dataPoint, then insert into the table.
        """
        pass

    @abc.abstractmethod
    def insertMany(self, dataPoints: List[Dict[str, JSONObject]]):
        """
        Check for validity of each dataPoint,then insert into the table.
        """
        pass
