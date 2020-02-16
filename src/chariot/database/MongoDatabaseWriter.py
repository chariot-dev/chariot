from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from typing import List, Type
from time import time

from chariot.JSONTypes import JSONDict
from chariot.database.DatabaseWriter import DatabaseWriter
from chariot.database.DatabaseConfiguration import DatabaseConfiguration
from chariot.database.MongoDatabaseConfiguration import MongoDatabaseConfiguration


class MongoDatabaseWriter(DatabaseWriter):
    def __init__(self, databaseConfiguration: Type[MongoDatabaseConfiguration]):
        super().__init__(databaseConfiguration)
        # self.databaseConfiguration: Type[MongoDatabaseConfiguration] = databaseConfiguration
        # self.configMap: JSONDict = self.databaseConfiguration.configMap
        # self.connect()
        # self.initializeTable()

    def __del__(self):
        self.disconnect()

    def connect(self):
        # Generate connection string based on config
        self.connectionString: str = 'mongodb://'
        if 'username' in self.configMap:
            self.connectionString += self.configMap['username'] + \
                ':' + self.configMap['password'] + '@'

        self.connectionString += self.configMap['host'] + \
            ':' + self.configMap['port']

        if 'database' in self.configMap:
            self.connectionString += '/' + self.configMap['database']
        else:
            self.configMap['database'] = 'iot_database'
            self.connectionString += '/' + self.configMap['database']

        # Create connection
        self.client: MongoClient = MongoClient(self.connectionString)

    def disconnect(self):
        self.client.close()

    def initializeTable(self):
        # Create a collection to insert to
        self.database: Database = self.client[self.configMap['database']]
        self.iot_database: Collection = self.database['iot_data']

    def insertOne(self, dataPoint: dict):
        DatabaseWriter.checkDataPoint(dataPoint)

        # Add database insertion time to dataPoint
        dataPoint['db_insertion_time'] = int(
            round(time() * 1000))  # Millis since epoch
        self.iot_database.insert_one(dataPoint)

    def insertMany(self, dataPoints: List[dict]):
        for dataPoint in dataPoints:
            DatabaseWriter.checkDataPoint(dataPoint)
            # Add database insertion time to dataPoint
            dataPoint['db_insertion_time'] = int(
                round(time() * 1000))  # Millis since epoch

        self.iot_database.insert_many(dataPoints)


config = MongoDatabaseConfiguration(
    {'databaseType': 'MongoDB', 'host': 'localhost', 'port': '27017', 'database': 'iot_database'})
writer = MongoDatabaseWriter(config)
writer.insertOne({'relative_time': 100, 'freeform': 'hi'})
