from core.databaseWriter.DatabaseWriterCreator import DatabaseWriterCreator
from core.databaseWriter import MongoDBWriter


class MongoDatabaseCreator(DatabaseWriterCreator):
    username = ""
    password = ""
    ipAdr = ""
    port = 0


    def __init__(self):
        self.username
        self.password
        self.ipAdr
        self.port
        self.socket

    def createDBWriter(self):
        return MongoDBWriter
