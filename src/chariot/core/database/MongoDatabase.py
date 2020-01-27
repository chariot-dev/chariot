from tinymongo import TinyMongoClient
import os
from datetime import datetime

from chariot.core.database.Database import Database


class MongoDatabase(Database):
    """
    Implements the Database parent class.
    Creates a MongoDB instance and writes rows to it.

    Usage:
    mongoDB = MongoDatabase()
    mongoDB.insertRow(1000, "json")
    """

    def __init__(self, db_path: str = 'mongo_database', flush: bool = False):
        Database.__init__(self, db_path=db_path, flush=flush)
        self.connectToDB()

    def initializeDB(self):
        self.db = self.conn.mydb
        self.collection = self.db.mycoll
        if self.flush:
            self.flushDB()

    def connectToDB(self):
        try:
            os.mkdir(self.db_path)
        except FileExistsError:
            pass
        os.chmod(self.db_path, 0o700)

        self.conn = TinyMongoClient(self.db_path)
        self.initializeDB()

    def disconnectFromDB(self):
        if self.conn:
            self.conn = None

    def insertRow(self, relative_time: int, freeform: str):
        row = dict()
        row['relative_time'] = relative_time
        row['freeform'] = freeform
        abs_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row['abs_time'] = abs_time
        self.collection.insert_one(row)

    def flushDB(self):
        self.collection.delete_many(query=None)

    # def prettyPrint(self):
