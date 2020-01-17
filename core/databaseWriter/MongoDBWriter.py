# TODO figure out import as module
from DatabaseWriter import DatabaseWriter
from tinymongo import TinyMongoClient
import os


class MongoDBWriter(DatabaseWriter):
    """
    Implements the DatabaseWriter parent class.
    Creates a MongoDB instance and writes rows to it.

    Usage:
    mongoWriter = MongoDBWriter()

    """

    def __init__(self, db_path='mongo_database', flush=False):
        DatabaseWriter.__init__(self, db_path=db_path, flush=flush)
        self.connectToDB()

    def initializeDB(self, conn):
        """
        Creates a new collection.
        """
        self.db = conn.mydb
        self.collection = self.db.mycoll
        if self.flush:
            self.flushDB()

    def connectToDB(self):
        """
        Create a new database if it does not exist, and generates a connection.

        Returns:
            A connection to the database.
        """
        try:
            os.mkdir(self.db_path)
        except FileExistsError:
            pass
        os.chmod(self.db_path, 0o700)

        self.conn = TinyMongoClient(self.db_path)
        self.initializeDB(self.conn)

        return self.conn

    def disconnectFromDB(self):
        """
        Deletes connection to the database.
        """
        if self.conn:
            self.conn = None

    def insertRow(self, data):
        """
        Insert a row into the database.

        Args:
            data: A Python dict.
        """
        self.collection.insert_one(data)

    def flushDB(self):
        """
        Remove all entries from the database.
        """
        self.collection.delete_many(query=None)


if __name__ == "__main__":
    entry = dict()
    entry["time"] = 15.1
    entry["freeform"] = dict()
    entry["freeform"]["temp"] = 72.0

    entry2 = dict()
    entry2["time"] = 16.0
    entry2["freeform"] = dict()
    entry2["freeform"]["balance"] = 120

    db = MongoDBWriter()
    db.connectToDB()
    db.insertRow(entry)
    db.insertRow(entry2)
    db.disconnectFromDB()
