from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from typing import List, Type, Dict
from time import time

from chariot.JSONTypes import JSONDict, JSONObject
from chariot.database.DatabaseWriter import DatabaseWriter
from chariot.database.DatabaseConfiguration import DatabaseConfiguration
from chariot.database.MongoDatabaseConfiguration import MongoDatabaseConfiguration


class MongoDatabaseWriter(DatabaseWriter):
    def __init__(self, databaseConfiguration: Type[MongoDatabaseConfiguration]):
        super().__init__(databaseConfiguration)

    def __del__(self):
        self.disconnect()

    def connect(self):
        # Generate connection string based on config
        self.connectionString: str = 'mongodb://'
        if hasattr(self.databaseConfiguration, 'username'):
            self.connectionString += self.databaseConfiguration.username + \
                ':' + self.databaseConfiguration.password + '@'
        self.connectionString += self.databaseConfiguration.host + \
            ':' + str(self.databaseConfiguration.port) + '/'
        if not hasattr(self.databaseConfiguration, 'database'):
            setattr(self.databaseConfiguration, 'database', 'iot_database')
        self.connectionString += self.databaseConfiguration.database

        # Create connection
        self.client: MongoClient = MongoClient(self.connectionString)

    def disconnect(self):
        self.client.close()

    def initializeTable(self):
        pass
        # Create a collection to insert to
        self.database: Database = self.client[self.databaseConfiguration.database]
        self.table: Collection = self.database['iot_data']

    def insertOne(self, dataPoint: Dict[str, JSONDict]):
        DatabaseWriter.checkDataPoint(dataPoint)

        # Add database insertion time to dataPoint
        dataPoint['db_insertion_time'] = int(
            round(time() * 1000))  # Millis since epoch
        self.table.insert_one(dataPoint)

    def insertMany(self, dataPoints: List[Dict[str, JSONDict]]):
        for dataPoint in dataPoints:
            DatabaseWriter.checkDataPoint(dataPoint)
            # Add database insertion time to dataPoint
            dataPoint['db_insertion_time'] = int(
                round(time() * 1000))  # Millis since epoch

        self.table.insert_many(dataPoints)