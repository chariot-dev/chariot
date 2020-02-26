from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from typing import Dict, List, Optional, Type
from time import time

from chariot.utility.JSONTypes import JSONDict, JSONObject
from chariot.database.writer.DatabaseWriter import DatabaseWriter
from chariot.database.configuration.DatabaseConfiguration import DatabaseConfiguration
from chariot.database.configuration.MongoDatabaseConfiguration import MongoDatabaseConfiguration


class MongoDatabaseWriter(DatabaseWriter):
    def __init__(self, config: MongoDatabaseConfiguration):
        super().__init__(config)
        self.client: Optional[MongoClient] = None
        self.table: Optional[Collection] = None

    def _connect(self):
        connectStr: str = 'mongodb://'
        if hasattr(self.config, 'username'):
            connectStr += f'{self.config.username}:{self.config.username}@'
        connectStr += f'{self.config.host}:{self.config.port}/{self.config.databaseName}'
        self.client = MongoClient(connectStr)

    def _disconnect(self):
        self.client.close()
        self.client = None

    def _initializeTable(self):
        database: Database = self.client[self.config.databaseName]
        self.table = database[self.config.tableName]

    def _insertOne(self, dataPoint: Dict[str, JSONObject]):
        dataPoint['db_insertion_time'] = int(round(time() * 1000))  # Millis since epoch
        self.table.insert_one(dataPoint)

    def _insertMany(self, dataPoints: List[Dict[str, JSONObject]]):
        for dataPoint in dataPoints:
            dataPoint['db_insertion_time'] = int(round(time() * 1000))  # Millis since epoch
        self.table.insert_many(dataPoints)
