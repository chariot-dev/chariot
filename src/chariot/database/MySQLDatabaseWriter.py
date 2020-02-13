from typing import List, Tuple
import mysql.connector as connector

from chariot.database.DatabaseWriter import DatabaseWriter


class MySQLDatabaseWriter(DatabaseWriter):
    def __init__(self, connectionString: str):
        '''
        Connection string should follow format:
        user:password@host:port
        '''
        # Parse connection string
        _user = connectionString.split('@')[0].split(':')[0]
        _password = connectionString.split('@')[0].split(':')[1]
        _host = connectionString.split('@')[1].split(':')[0]
        _port = connectionString.split('@')[1].split(':')[1]

        self.connect(_user, _password, _host, _port)

    def __del__(self):
        self.disconnect()

    def connect(self, _user: str, _password: str, _host: str, _port: int):
        self.conn: connector.connection.MySQLConnection = connector.connect(
            user=_user, password=_password, host=_host, port=_port)
        self.cursor: connector.cursor.MySQLCursor = self.conn.cursor()

    def disconnect(self):
        self.conn.close()

    def initializeTable(self):
        # Create a new database, to be safe
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS iot_data;")
        self.cursor.execute("USE iot_data;")
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
