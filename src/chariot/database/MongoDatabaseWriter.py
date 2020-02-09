from pymongo import MongoClient
from pymongo.collection import Collection
from typing import List

from chariot.database.DatabaseWriter import DatabaseWriter


class MongoDatabaseWriter(DatabaseWriter):
    def __init__(self, connectionString: str):
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
        DatabaseWriter.insertOne(self, dataPoint)
        self.iot_database.insert_one(dataPoint)

    def insertMany(self, dataPoints: List[dict]):
        DatabaseWriter.insertMany(self, dataPoints)
        self.iot_database.insert_many(dataPoints)


# Testing
# mdb = MongoDatabaseWriter('mongodb://localhost:27017/iot_data')
# mdb.initializeTable()
# rows = []
# for i in range(100):
#     rows.append({'relative_time': i, 'freeform': 'hi'})
# mdb.insertMany(rows)
# del(mdb)
