from typing import Dict, Type

from chariot.database.DatabaseWriter import DatabaseWriter
from chariot.database.MongoDatabaseWriter import MongoDatabaseWriter
from chariot.database.MySQLDatabaseWriter import MySQLDatabaseWriter
from chariot.database.DatabaseConfiguration import DatabaseConfiguration


class _DatabaseWriterFactory:
    def __init__(self):
        self.databaseMap: Dict[str, Type[DatabaseWriter]] = {
            'MongoDB': MongoDatabaseWriter,
            'MySQL': MySQLDatabaseWriter
        }

    def getInstance(self, databaseConfiguration: Type[DatabaseConfiguration]) -> Type[DatabaseWriter]:
        databaseType: str = databaseConfiguration.databaseType
        if databaseType not in self.databaseMap:
            raise AssertionError('Database type not supported')

        instance: Type[DatabaseWriter] = self.databaseMap[databaseType](databaseConfiguration)
        return instance


# Return singleton
DatabaseWriterFactory = _DatabaseWriterFactory()
