from core.databaseWriter.DatabaseWriterCreator import DatabaseWriterCreator
from core.databaseWriter.MySqlDBWriter import MySqlDBWriter


class MySqlDatabaseCreator(DatabaseWriterCreator):
    def __init__(self):
        self.username
        self.password
        self.ipAdr
        self.port
        self.socket

    def createDBWriter(self):
        return MySqlDBWriter
