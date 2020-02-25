import abc
from typing import Dict, List, Type

from chariot.database.configuration.DatabaseConfiguration import DatabaseConfiguration
from chariot.utility.JSONTypes import JSONObject


class DatabaseWriter(metaclass=abc.ABCMeta):
    validDataFields: Dict[str, Type[JSONObject]] = {
        'relative_time': str,
        'freeform': Type[JSONObject],
    }

    def __init__(self, config: Type[DatabaseConfiguration]):
        self.config: Type[DatabaseConfiguration] = config
        self.connected: bool = False
        self.connect()
        self.initializeTable()

    def __del__(self):
        self.disconnect()

    def connect(self, reconnect=False):
        """
        Establish a connection to the database.
        """
        if reconnect or not self.connected:
            self._connect()
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

    def initializeTable(self):
        """
        Create a table in the database.
        """
        if not self.connected:
            raise AssertionError
        self._initializeTable()

    @abc.abstractmethod
    def _initializeTable(self):
        pass

    def insertOne(self, dataPoint: Dict[str, JSONObject]):
        """
        Check for validity of dataPoint, then insert into the table.
        """
        if not self.connected:
            raise AssertionError
        self.validateDataPoint(dataPoint)
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
