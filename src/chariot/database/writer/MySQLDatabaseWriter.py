from mysql import connector
from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from chariot.utility.JSONTypes import JSONObject
from chariot.database.writer import DatabaseWriter
from chariot.database.configuration import MySQLDatabaseConfiguration
from typing import Dict, List, Optional


class MySQLDatabaseWriter(DatabaseWriter):
    def __init__(self, config: MySQLDatabaseConfiguration):
        super().__init__(config)
        self.connection: Optional[MySQLConnection] = None
        self.cursor: Optional[MySQLCursor] = None

    def _connect(self):
        self.connection = connector.connect(
            user=self._config.username,
            password=self._config.password,
            host=self._config.host,
            port=self._config.port,
            database=self._config.databaseName,
            connection_timeout=round(self._config.timeoutMS / 1000)
        )
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
        else:
            raise RuntimeError('Could not connect to database')

    def _disconnect(self):
        self.connection.close()

    def _initializeTable(self):
        self.cursor.execute(
            f'CREATE TABLE IF NOT EXISTS {self._config.tableName}(id INTEGER PRIMARY KEY AUTO_INCREMENT,\
             device_name VARCHAR(255), insertion_time BIGINT, production_time BIGINT, freeform VARBINARY(64535))'
        )

    def _insertOne(self, record: Dict[str, JSONObject]):
        self.cursor.execute(
            f'INSERT INTO {self._config.tableName} (device_name, insertion_time,\
             production_time, freeform) VALUES (%s, %s, %s, %s)',
            (record['device_name'], record['insertion_time'], record['production_time'], record['freeform'])
        )
        self.connection.commit()

    def _insertMany(self, records: List[Dict[str, JSONObject]]):
        self.cursor.executemany(
            f'INSERT INTO {self._config.tableName} (device_name, insertion_time,\
             production_time, freeform) VALUES (%s, %s, %s, %s)',
            ((record['device_name'], record['insertion_time'], record['production_time'],
              record['freeform']) for record in records)
        )
        self.connection.commit()
