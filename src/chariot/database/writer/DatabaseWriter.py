import abc
from typing import Dict, List, Type

from chariot.database.DatabaseConfiguration import DatabaseConfiguration
from chariot.utility.JSONTypes import JSONDict, JSONObject


class DatabaseWriter(metaclass=abc.ABCMeta):
    requiredFields: Dict[str, Type[JSONObject]] = {
        'relative_time': str,
        'freeform': Type[JSONObject],
    }

    def __init__(self, databaseConfiguration: Type[DatabaseConfiguration]):
        self.databaseConfiguration: Type[DatabaseConfiguration] = databaseConfiguration
        self.connect()
        self.initializeTable()

    def validateDataPoint(self, dataPoint: Dict[str, JSONObject]):
        """
        Check for validity of a dataPoint. dataPoint should have keys
        "relative_time" and "freeform". If dataPoint is missing either,
        or if it has extra keys, this function raises a ValueError.
        """
        for key in self.requiredFields:
            if key not in dataPoint:
                raise AssertionError(f'the field "{key}" is missing from the data point')
        for key in dataPoint:
            if key not in self.requiredFields:
                raise AssertionError(f'an invalid field "{key}" was included in the data point')

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
