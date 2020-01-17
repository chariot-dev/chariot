# TODO export as package
# from core.databaseWriter.DatabaseWriter import DatabaseWriter
from DatabaseWriter import DatabaseWriter
import mysql.connector


class MySqlDBWriter(DatabaseWriter):
    """
        The purpose of MySqlDBWriter is to interact with a MySQL db.
        Therefore, this class should be used whenever a write to a
        MySQL db is done. This class implements the DatabaseWriter class
    """

    def initializeDB(self):
        db = mysql.connector.connect(
            host="localhost",
            user="chariot",
            passwd=""
        )
        cursor = db.cursor()
        cursor.execute("CREATE DATABASE ChariotData")

    def connectToDB(self):
        pass

    def disconnectFromDB(self):
        pass

    def insertRow(self, data):
        pass

    def flushDB(self):
        pass


if __name__ == '__main__':
    db = MySqlDBWriter()
    db.initializeDB()
