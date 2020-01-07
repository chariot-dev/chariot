from core.databaseWriter.DatabaseWriter import DatabaseWriter

class MySqlDBWriter(DatabaseWriter):
    """
        The purpose of MySqlDBWriter is to interact with a MySQL db. Therefore, this class should
            be used whenever a write to a MySQL db is done. This class implements the DatabaseWriter class
    """

    def writeToDB(self):
        pass

    def connectToDB(self):
        pass

    def disconnectFromDB(self):
        pass