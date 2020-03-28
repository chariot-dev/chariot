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
        self.cursor: Optional[Cursor] = None
        self.clientPath: Optional[str] = None

    def __del__(self):
        self.cleanup()

    def cleanup(self):
        if self.client is not None:
            self.client.close()
            self.cursor = None
            self.client = None
            os.remove(self.clientPath)
            os.removedirs('/'.join(self.clientPath.split('/')[:-1]))

    def _connect(self) -> None:
        currentPath: str = os.path.dirname(os.path.abspath(__file__))
        dbPath: str = f'{currentPath}/temp'
        os.makedirs(dbPath, 0o777, exist_ok=True)
        self.clientPath = f'{dbPath}/{self._config.databaseName}.db'
        self.client = sqlite3.connect(self.clientPath, check_same_thread=False)
        self.cursor = self.client.cursor()

    def _disconnect(self) -> None:
        pass

    def getCursor(self) -> Optional[Cursor]:
        return self.cursor

    def _initializeTable(self) -> None:
        self.cursor.execute(
            f'CREATE TABLE IF NOT EXISTS {self._config.tableName}(id INTEGER PRIMARY KEY AUTOINCREMENT, device_name VARCHAR(255), insertion_time INTEGER, production_time INTEGER, freeform BLOB)'
        )

    def _insertOne(self, record: Dict[str, JSONObject]) -> None:
        pass

    def _insertMany(self, records: List[Dict[str, JSONObject]]) -> None:
        self.cursor.executemany(
            f'INSERT INTO {self._config.tableName} (device_name, insertion_time, production_time, freeform) VALUES (?,?,?,?)',
            ((record['device_name'], record['insertion_time'], record['production_time'], self._pickleFreeform(record['freeform'])) for record in records)
        )
        self.client.commit()

    def _pickleFreeform(self, freeform: JSONObject):
        return sqlite3.Binary(pickle.dumps(freeform, pickle.HIGHEST_PROTOCOL)) 
