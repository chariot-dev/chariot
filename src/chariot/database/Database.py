import abc
from typing import List


class Database(metaclass=abc.ABCMeta):
    def __init__(self, db_path: str = '../data/iot_database.db'):
        self.db_path = db_path

    @abc.abstractmethod
    def initializeDB(self):
        """
        Create the necessary table in the database
        """
        pass

    @abc.abstractmethod
    def connectToDB(self):
        """
        Establish a database connection
        """
        pass

    @abc.abstractmethod
    def deleteDB(self):
        """
        Delete the database file
        """
        pass

    @abc.abstractmethod
    def disconnectFromDB(self):
        """
        Delete the database connection
        """
        pass

    @abc.abstractmethod
    def insertOne(self, dataPoint: dict):
        """
        Check for validity of dataPoint, then insert into database
        """
        if sorted(dataPoint.keys()) != sorted(['relative_time', 'freeform']):
            raise ValueError('Data point has incorrect keys')

    @abc.abstractmethod
    def insertMany(self, dataPoints: List[dict]):
        """
        Check for validity of dataPoints, then insert into database
        """
        for dataPoint in dataPoints:
            if sorted(dataPoint.keys()) != sorted(
                    ['relative_time', 'freeform']):
                raise ValueError('Data point has incorrect keys')

    @abc.abstractmethod
    def flush(self):
        """
        Delete all rows from database
        """
        pass
