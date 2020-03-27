from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from typing import Dict, List, Optional
from chariot.utility.JSONTypes import JSONObject
from chariot.database.writer import DatabaseWriter
from chariot.database.configuration import DatabaseConfiguration, MongoDatabaseConfiguration


class MongoDatabaseWriter(DatabaseWriter):
    def __init__(self, config: MongoDatabaseConfiguration):
        super().__init__(config)
        self.client: Optional[MongoClient] = None
        self.table: Optional[Collection] = None

    def _connect(self):
        connectStr: str = 'mongodb://'
        if hasattr(self.config, 'username'):
            connectStr += f'{self.config.username}:{self.config.password}@'
        connectStr += f'{self.config.host}:{self.config.port}/{self.config.databaseName}'
        self.client = MongoClient(
            connectStr,
            serverSelectionTimeoutMS=self.config.timeoutMS)
        self.client.server_info()  # This will raise error if connection invalid

    def _disconnect(self):
        self.client.close()
        self.client = None

    def _initializeTable(self):
        database: Database = self.client[self.config.databaseName]
        self.table = database[self.config.tableName]

    def _insertOne(self, record: Dict[str, JSONObject]):
        self.table.insert_one(record)

    def _insertMany(self, records: List[Dict[str, JSONObject]]):
        self.table.insert_many(records)
