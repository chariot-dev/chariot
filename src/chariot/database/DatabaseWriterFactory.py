from chariot.database.DatabaseWriter import DatabaseWriter
from chariot.database.MongoDatabaseWriter import MongoDatabaseWriter
from chariot.database.MySQLDatabaseWriter import MySQLDatabaseWriter


class DatabaseWriterFactory:
    def GetDatabaseWriter(DatabaseWriterType: str, connectionString: str) -> DatabaseWriter:
        if DatabaseWriterType == 'MONGODB':
            return MongoDatabaseWriter(connectionString)
        elif DatabaseWriterType == 'MYSQL':
            return MySQLDatabaseWriter(connectionString)
        else:
            return None
