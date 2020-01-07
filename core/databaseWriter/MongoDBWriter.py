from core.databaseWriter.DatabaseWriter import DatabaseWriter


class MongoDBWriter(DatabaseWriter):

    """
    The purpose of MongoDBWriter is to interact with a MongoDB. Therefore, this class should
        be used whenever a write to a MongoDB is done. This class implements the DatabaseWriter class
    """

    """
    def __init__(self):
        "TODO: figure out how to get JSON passed to this via REST PROTOCOL"
    """

    def writeToDB(self):
        pass

    def connectToDB(self):
        pass

    def disconnectFromDB(self):
        pass