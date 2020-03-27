import abc
from multiprocessing import Lock
from typing import Dict, List, Type
from time import time
from chariot.database.configuration import DatabaseConfiguration
from chariot.utility.JSONTypes import JSONObject


class DatabaseWriter(metaclass=abc.ABCMeta):
    validDataFields: Dict[str, Type[JSONObject]] = {
        'device_name': str,
        'production_time': int,
        'freeform': Type[JSONObject],
    }

    def __init__(self, config: Type[DatabaseConfiguration]):
        self.config: Type[DatabaseConfiguration] = config
        self.connected: bool = False
        self.writeLock: Lock = Lock()

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

    def getConfiguration(self):
        return self.config

    @abc.abstractmethod
    def _initializeTable(self):
        pass

    def insertOne(self, record: Dict[str, JSONObject]):
        """
        Check for validity of record, add insertion_time field, then insert into the table.
        """
        if not self.connected:
            raise AssertionError
        self.validateRecord(record)
        record['insertion_time'] = int(round(time() * 1000))
        with self.writeLock:
            self._insertOne(record)

    @abc.abstractmethod
    def _insertOne(self, records: List[Dict[str, JSONObject]]):
        pass

    def insertMany(self, records: List[Dict[str, JSONObject]]):
        """
        Check for validity of each record, then insert into the table.
        """
        if not self.connected:
            raise AssertionError
        for record in records:
            self.validateRecord(record)
            record['insertion_time'] = int(round(time() * 1000))
        with self.writeLock:
            self._insertMany(records)

    @abc.abstractmethod
    def _insertMany(self, records: List[Dict[str, JSONObject]]):
        pass

    def isConnected(self) -> bool:
        return self.connected

    def validateRecord(self, record: Dict[str, JSONObject]):
        for key in self.validDataFields:
            if key not in record:
                raise AssertionError(f'the field "{key}" is missing from the data point')
        for key in record:
            if key not in self.validDataFields:
                raise AssertionError(f'an invalid field "{key}" was included in the data point')
