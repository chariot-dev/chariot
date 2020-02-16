from typing import List, Tuple, Type
import mysql.connector as connector

from chariot.JSONTypes import JSONDict
from chariot.database.DatabaseWriter import DatabaseWriter
from chariot.database.DatabaseConfiguration import DatabaseConfiguration
from chariot.database.MySQLDatabaseConfiguration import MySQLDatabaseConfiguration


class MySQLDatabaseWriter(DatabaseWriter):
    def __init__(self, databaseConfiguration: Type[MySQLDatabaseConfiguration]):
        super().__init__(databaseConfiguration)

    def __del__(self):
        self.disconnect()

    def connect(self):
        self.conn: connector.connection.MySQLConnection = connector.connect(
            user=self.configMap['username'],
            password=self.configMap['password'],
            host=self.configMap['host'],
            port=self.configMap['port'],
            database=self.configMap['database']
        )

        self.cursor: connector.cursor.MySQLCursor = self.conn.cursor()

    def disconnect(self):
        self.conn.close()

    def initializeTable(self):
        # Create a new database, to be safe
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS data(id INTEGER PRIMARY KEY AUTO_INCREMENT, db_insertion_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, relative_time BIGINT, freeform VARBINARY(64535))"
        )

    def insertOne(self, dataPoint: dict):
        DatabaseWriter.checkDataPoint(dataPoint)
        self.cursor.execute(
            "INSERT INTO data (relative_time, freeform) VALUES (%s, %s)",
            (dataPoint["relative_time"], dataPoint["freeform"])
        )

        self.conn.commit()

    def insertMany(self, dataPoints: List[dict]):
        for dataPoint in dataPoints:
            DatabaseWriter.checkDataPoint(dataPoint)

        values_to_insert: List[Tuple[int, str]] = [(dataPoint["relative_time"], dataPoint["freeform"])
                                                   for dataPoint in dataPoints]
        self.cursor.executemany(
            "INSERT INTO data (relative_time, freeform) VALUES (%s, %s)",
            values_to_insert
        )

        self.conn.commit()


config = MySQLDatabaseConfiguration(
    {
        'databaseType': 'MySQL',
        'host': 'localhost',
        'port': '3306',
        'database': 'iot_data',
        'username': 'root',
        'password': '5431'})
writer = MySQLDatabaseWriter(config)
