import abc
from typing import Dict, List, Type
from time import time

from chariot.database.configuration import DatabaseConfiguration
from chariot.utility.JSONTypes import JSONObject


class DatabaseWriter(metaclass=abc.ABCMeta):
    validDataFields: Dict[str, Type[JSONObject]] = {
        'relative_time': str,
        'freeform': Type[JSONObject],
    }

    def __init__(self, config: Type[DatabaseConfiguration]):
        self.config: Type[DatabaseConfiguration] = config
        self.connected: bool = False

    def __del__(self):
        self.disconnect()

    def connect(self, reconnect: bool = False):
        """
        Establish a connection to the database.
        """
        if reconnect or not self.connected:
            self._connect()
            self._initializeTable()
            self.connected = True

    @abc.abstractmethod
    def _connect(self):
        pass

    def disconnect(self):
        """
        End connection to the database gracefully.
        """
        if self.connected:
            self._disconnect()
        self.connected = False

    @abc.abstractmethod
    def _disconnect(self):
        pass

    @abc.abstractmethod
    def _initializeTable(self):
        pass

    def insertOne(self, dataPoint: Dict[str, JSONObject]):
        """
        Check for validity of dataPoint, add insertion_time field, then insert into the table.
        """
        if not self.connected:
            raise AssertionError
        self.validateDataPoint(dataPoint)
        dataPoint['insertion_time'] = int(
            round(time() * 1000))  # Millis since epoch
        self._insertOne(dataPoint)

    @abc.abstractmethod
    def _insertOne(self):
        pass

    def insertMany(self, dataPoints: List[Dict[str, JSONObject]]):
        """
        Check for validity of each dataPoint,then insert into the table.
        """
        if not self.connected:
            raise AssertionError
        for dataPoint in dataPoints:
            self.validateDataPoint(dataPoint)
            dataPoint['insertion_time'] = int(
                round(time() * 1000))  # Millis since epoch
        self._insertMany(dataPoints)

    @abc.abstractmethod
    def _insertMany(self):
        pass

    def validateDataPoint(self, dataPoint: Dict[str, JSONObject]):
        for key in self.validDataFields:
            if key not in dataPoint:
                raise AssertionError(f'the field "{key}" is missing from the data point')
        for key in dataPoint:
            if key not in self.validDataFields:
                raise AssertionError(f'an invalid field "{key}" was included in the data point')
