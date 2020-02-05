import sqlite3
import csv
import os
from typing import List

from chariot.database.Database import Database


class SQLiteDatabase(Database):
    def __init__(self, db_path: str = '../data/iot_database.db'):
        Database.__init__(self, db_path)
        self.connectToDB()

    def initializeDB(self):
        cursor = self.conn.cursor()
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS IOTD('
            'id INTEGER PRIMARY KEY, ' +
            'db_insertion_time DATETIME DEFAULT CURRENT_TIMESTAMP, ' +
            'relative_time BIGINT, ' +
            'freeform TEXT)')
        self.conn.commit()

    def connectToDB(self):
        # Make the data directory if it does not exist
        dirname = os.path.dirname(self.db_path)
        try:
            os.makedirs(dirname)
        except FileExistsError:
            pass
        self.conn = sqlite3.connect(self.db_path)
        os.chmod(self.db_path, 0o600)
        self.initializeDB()

    def deleteDB(self):
        os.remove(self.db_path)

    def disconnectFromDB(self):
        self.conn = None

    def insertOne(self, dataPoint: dict):
        Database.insertOne(self, dataPoint)
        cursor = self.conn.cursor()
        cursor.execute(
            'INSERT INTO IOTD (relative_time, freeform) VALUES (?, ?)',
            (dataPoint['relative_time'], dataPoint['freeform'])
        )
        self.conn.commit()

    def insertMany(self, dataPoints: List[dict]):
        Database.insertMany(self, dataPoints)

        # Create list of (relative_time, freeform) tuples for every dataPoint
        insertList = [(dataPoint['relative_time'], dataPoint['freeform'])
                      for dataPoint in dataPoints]
        cursor = self.conn.cursor()
        cursor.executemany(
            'INSERT INTO IOTD (relative_time, freeform) VALUES (?, ?)',
            insertList
        )

    def flush(self):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM IOTD')
        self.conn.commit()

    def toCSV(self, outfile='../data/iot_database.csv'):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM IOTD')
        with open(outfile, 'w') as out:
            csv_writer = csv.writer(out, delimiter=",")
            csv_writer.writerow(i[0] for i in cursor.description)
            csv_writer.writerows(cursor)
