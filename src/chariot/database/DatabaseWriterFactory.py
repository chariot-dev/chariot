from typing import Dict, Type

from chariot.database.DatabaseWriter import DatabaseWriter
from chariot.database.MongoDatabaseWriter import MongoDatabaseWriter
from chariot.database.MySQLDatabaseWriter import MySQLDatabaseWriter
from chariot.database.DatabaseConfiguration import DatabaseConfiguration
from chariot.database.MySQLDatabaseConfiguration import MySQLDatabaseConfiguration


class _DatabaseWriterFactory:
    def __init__(self):
        self.deviceMap: Dict[str, Type[DatabaseWriter]] = {
            'MongoDB': MongoDatabaseWriter,
            'MySQL': MySQLDatabaseWriter
        }

    def getInstance(self, databaseConfiguration: Type[DatabaseConfiguration]) -> Type[DatabaseWriter]:
        databaseType: str = databaseConfiguration.databaseType
        if databaseType not in self.deviceMap:
            raise AssertionError('Database type not supported')

        instance: Type[DatabaseWriter] = self.deviceMap[databaseType](databaseConfiguration)
        return instance


# Return singleton
DatabaseWriterFactory = _DatabaseWriterFactory()
