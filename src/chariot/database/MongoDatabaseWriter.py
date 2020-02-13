from pymongo import MongoClient
from pymongo.collection import Collection
from typing import List
from time import time

from chariot.database.DatabaseWriter import DatabaseWriter, checkDataPoint


class MongoDatabaseWriter(DatabaseWriter):
    def __init__(self, connectionString: str):
        '''
        Connection string should follow Mongo URI format:
        https://docs.mongodb.com/manual/reference/connection-string/
        Eg. for localhost: 'mongodb://localhost:27017/'
        '''
        self.connectionString: str = connectionString
        self.connect()

    def __del__(self):
        self.disconnect()

    def connect(self):
        self.client: MongoClient = MongoClient(self.connectionString)

    def disconnect(self):
        self.client.close()

    def initializeTable(self):
        # Create a collection to insert to
        self.iot_database: Collection = self.client["iot_database"]["iot_data"]

    def insertOne(self, dataPoint: dict):
        checkDataPoint(dataPoint)

        # Add database insertion time to dataPoint
        dataPoint['db_insertion_time'] = int(
            round(time.time() * 1000))  # Millis since epoch
        self.iot_database.insert_one(dataPoint)

    def insertMany(self, dataPoints: List[dict]):
        for dataPoint in dataPoints:
            checkDataPoint(dataPoint)
            # Add database insertion time to dataPoint
            dataPoint['db_insertion_time'] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S")
            dataPoint['db_insertion_time'] = datetime.now()

        self.iot_database.insert_many(dataPoints)
