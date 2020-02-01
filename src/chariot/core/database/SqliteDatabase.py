import sqlite3
import os
import csv

from chariot.core.database.Database import Database


class SqliteDatabase(Database):
    """
    Implements the Database parent class.
    Creates a Sqlite database and writes to it.

    Usage:
    sqliteDB = SqliteDatabase()
    sqliteDB.insertRow(1000, "json")
    """

    def __init__(self, db_path: str = 'database.db', flush: bool = False):
        Database.__init__(self, db_path=db_path, flush=flush)
        self.connectToDB()
        if self.flush:
            self.flushDB()

    def initializeDB(self):
        cursor = self.conn.cursor()
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS IOTD('
            'id INTEGER PRIMARY KEY, ' +
            'abs_time DATETIME DEFAULT CURRENT_TIMESTAMP, ' +
            'relative_time BIGINT, ' +
            'freeform TEXT)')
        self.conn.commit()

    def connectToDB(self):
        self.conn = sqlite3.connect(self.db_path)
        os.chmod(self.db_path, 0o600)
        self.initializeDB()

    def disconnectFromDB(self):
        if self.conn:
            self.conn = None

    def insertRow(self, relative_time: int, freeform: str):
        rowlist = (relative_time, freeform)
        cursor = self.conn.cursor()
        cursor.execute(
            '''INSERT INTO IOTD (relative_time, freeform) VALUES (?, ?)''',
            rowlist)
        self.conn.commit()

    def flushDB(self):
        cursor = self.conn.cursor()
        cursor.execute('''DELETE FROM IOTD;''')
        self.conn.commit()

    def toCSV(self, outfile='database.csv'):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM IOTD''')
        with open(outfile, 'w') as out:
            csv_writer = csv.writer(out, delimiter=",")
            csv_writer.writerow(i[0] for i in cursor.description)
            csv_writer.writerows(cursor)
