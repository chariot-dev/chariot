from tinymongo import TinyMongoClient
import os
from datetime import datetime
from typing import List
import shutil

from chariot.database.Database import Database


class MongoDatabase(Database):
    def __init__(self, db_path: str = '../data/iot_database'):
        Database.__init__(self, db_path=db_path)
        self.connectToDB()

    def initializeDB(self):
        self.database = self.conn.database
        self.collection = self.database.collection

    def connectToDB(self):
        # Make the data directory if it does not exist
        try:
            os.makedirs(self.db_path)
        except FileExistsError:
            pass
        os.chmod(self.db_path, 0o700)

        self.conn = TinyMongoClient(self.db_path)
        self.initializeDB()

    def deleteDB(self):
        shutil.rmtree(self.db_path)

    def disconnectFromDB(self):
        self.conn = None

    def insertOne(self, dataPoint: dict):
        Database.insertOne(self, dataPoint)
        db_insertion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dataPoint['db_insertion_time'] = db_insertion_time
        self.collection.insert_one(dataPoint)

    def insertMany(self, dataPoints: List[dict]):
        Database.insertMany(self, dataPoints)
        db_insertion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for dataPoint in dataPoints:
            dataPoint['db_insertion_time'] = db_insertion_time
        self.collection.insert_many(dataPoints)

    def flush(self):
        self.collection.delete_many(query=None)
