from typing import List, Tuple
import mysql.connector as connector

from chariot.database.DatabaseWriter import DatabaseWriter


class MySQLDatabaseWriter(DatabaseWriter):
    def __init__(self, _user: str, _password: str, _host: str, _port: int):
        self.connect(_user, _password, _host, _port)

    def __del__(self):
        self.disconnect()

    def connect(self, _user: str, _password: str, _host: str, port: int):
        self.conn: connector.connection.MySQLConnection = connector.connect(
            user=_user, password=_password, host=_host)
        self.cursor: connector.cursor.MySQLCursor = self.conn.cursor()

    def disconnect(self):
        pass

    def initializeTable(self):
        # Create a new database, to be safe
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS iot_data;")
        self.cursor.execute("USE iot_data;")
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS data(id INTEGER PRIMARY KEY AUTO_INCREMENT, db_insertion_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, relative_time BIGINT, freeform VARBINARY(64535))"
        )

    def insertOne(self, dataPoint: dict):
        DatabaseWriter.insertOne(self, dataPoint)
        self.cursor.execute(
            "INSERT INTO data (relative_time, freeform) VALUES (%s, %s)",
            (dataPoint["relative_time"], dataPoint["freeform"])
        )

        self.conn.commit()

    def insertMany(self, dataPoints: List[dict]):
        DatabaseWriter.insertMany(self, dataPoints)
        values_to_insert: List[Tuple[int, str]] = [(dataPoint["relative_time"], dataPoint["freeform"])
                                                   for dataPoint in dataPoints]
        self.cursor.executemany(
            "INSERT INTO data (relative_time, freeform) VALUES (%s, %s)",
            values_to_insert
        )

        self.conn.commit()
