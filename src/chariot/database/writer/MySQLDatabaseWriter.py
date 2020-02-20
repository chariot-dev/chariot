from mysql import connector
from mysql.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from chariot.utility.JSONTypes import JSONDict, JSONObject
from chariot.database.writer.DatabaseWriter import DatabaseWriter
from chariot.database.configuration.DatabaseConfiguration import DatabaseConfiguration
from chariot.database.configuration.MySQLDatabaseConfiguration import MySQLDatabaseConfiguration
from typing import Dict, List, Tuple, Type, Union


class MySQLDatabaseWriter(DatabaseWriter):
    def __init__(self, config: MySQLDatabaseConfiguration):
        super().__init__(config)
        self.connection: Union[MySQLConnection, None] = None
        self.cursor: Union[MySQLCursor, None] = None

    def _connect(self):
        self.connection = connector.connect(
            user=self.config['username'],
            password=self.config['password'],
            host=self.config['host'],
            port=self.config['port'],
            database=self.config['databaseName']
        )
        self.cursor = self  .connection.cursor()
        self.connected = True

    def _disconnect(self):
        self.connection.close()

    def _initializeTable(self):
        self.cursor.execute(
            f'CREATE TABLE IF NOT EXISTS {self.config["tableName"]}' + 
            '(id INTEGER PRIMARY KEY AUTO_INCREMENT, db_insertion_time TIMESTAMP DEFAULT UNIX_TIMESTAMP(), relative_time BIGINT, freeform VARBINARY(64535))'
        )

    def _insertOne(self, dataPoint: Dict[str, JSONObject]):
        self.cursor.execute(
            f'INSERT INTO {self.tableName} (relative_time, freeform) VALUES (%s, %s)',
            (dataPoint['relative_time'], dataPoint['freeform'])
        )
        self.connection.commit()

    def _insertMany(self, dataPoints: List[Dict[str, JSONObject]]):
        self.cursor.executemany(
            f'INSERT INTO {self.tableName} (relative_time, freeform) VALUES (%s, %s)',
            [(dataPoint['relative_time'], dataPoint['freeform']) for dataPoint in dataPoints]
        )
        self.connection.commit()
