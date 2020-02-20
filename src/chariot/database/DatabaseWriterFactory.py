from typing import Dict, Type
from chariot.database.writer.DatabaseWriter import DatabaseWriter
from chariot.database.writer.MongoDatabaseWriter import MongoDatabaseWriter
from chariot.database.writer.MySQLDatabaseWriter import MySQLDatabaseWriter
from chariot.database.configuration.DatabaseConfiguration import DatabaseConfiguration
from chariot.utility.AbstractFactory import AbstractFactory


class _DatabaseWriterFactory(AbstractFactory):
    def __init__(self):
        self.instanceMap: Dict[str, Type[DatabaseWriter]] = {
            'MongoDB': MongoDatabaseWriter,
            'MySQL': MySQLDatabaseWriter
        }
        self.instanceName: str = 'database'


# Return singleton
DatabaseWriterFactory = _DatabaseWriterFactory()

__all__ = ['DatabaseWriterFactory']
