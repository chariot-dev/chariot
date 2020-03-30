import pickle
from multiprocessing import Lock
import os
import sqlite3
from sqlite3 import Connection, Cursor
from typing import Dict, Optional, List
from chariot.database.configuration import DatabaseConfiguration
from chariot.database.writer import DatabaseWriter
from chariot.utility.JSONTypes import JSONObject

class TestDatabaseWriter(DatabaseWriter):
    def __init__(self, config: DatabaseConfiguration):
        super().__init__(config)
        self.client: Optional[Connection] = None
        self.clientPath: Optional[str] = None

    def __del__(self):
        self.cleanup()

    def cleanup(self):
        if self.client is not None:
            self.client.close()
            self.client = None
            os.remove('testdb')

    def _connect(self) -> None:
        self.client = sqlite3.connect('testdb', check_same_thread=False)

    def _disconnect(self) -> None:
        pass

    def getClient(self) -> Optional[Connection]:
        return self.client

    def _initializeTable(self) -> None:
        with self.client:
            self.client.execute(
                f'CREATE TABLE IF NOT EXISTS {self._config.tableName}(id INTEGER PRIMARY KEY AUTOINCREMENT, device_name VARCHAR(255), insertion_time INTEGER, production_time INTEGER, freeform BLOB)'
            )

    def _insertOne(self, record: Dict[str, JSONObject]) -> None:
        pass

    def _insertMany(self, records: List[Dict[str, JSONObject]]) -> None:
        with self.client:
            self.client.executemany(
                f'INSERT INTO {self._config.tableName} (device_name, insertion_time, production_time, freeform) VALUES (?,?,?,?)',
                ((record['device_name'], record['insertion_time'], record['production_time'], self._pickleFreeform(record['freeform'])) for record in records)
            )

    def _pickleFreeform(self, freeform: JSONObject):
        return memoryview(pickle.dumps(freeform))
