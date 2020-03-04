from mysql import connector
from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from chariot.utility.JSONTypes import JSONObject
from chariot.database.writer import DatabaseWriter
from chariot.database.configuration import DatabaseConfiguration, MySQLDatabaseConfiguration
from typing import Dict, List, Optional


class MySQLDatabaseWriter(DatabaseWriter):
    def __init__(self, config: MySQLDatabaseConfiguration):
        super().__init__(config)
        self.connection: Optional[MySQLConnection] = None
        self.cursor: Optional[MySQLCursor] = None

    def _connect(self):
        self.connection = connector.connect(
            user=self.config.username,
            password=self.config.password,
            host=self.config.host,
            port=self.config.port,
            database=self.config.databaseName,
            connection_timeout=round(self.config.timeoutMS / 1000)
        )
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
        else:
            raise RuntimeError('Could not connect to database')

    def _disconnect(self):
        self.connection.close()

    def _initializeTable(self):
        self.cursor.execute(
            f'CREATE TABLE IF NOT EXISTS {self.config.tableName}(id INTEGER PRIMARY KEY AUTO_INCREMENT, insertion_time BIGINT, relative_time BIGINT, freeform VARBINARY(64535))'
        )

    def _insertOne(self, dataPoint: Dict[str, JSONObject]):
        self.cursor.execute(
            f'INSERT INTO {self.config.tableName} (relative_time, insertion_time, freeform) VALUES (%s, %s, %s)',
            (dataPoint['relative_time'], dataPoint['insertion_time'], dataPoint['freeform'])
        )
        self.connection.commit()

    def _insertMany(self, dataPoints: List[Dict[str, JSONObject]]):
        self.cursor.executemany(
            f'INSERT INTO {self.config.tableName} (relative_time, insertion_time, freeform) VALUES (%s, %s, %s)',
            [(dataPoint['relative_time'], dataPoint['insertion_time'], dataPoint['freeform']) for dataPoint in dataPoints]
        )
        self.connection.commit()
