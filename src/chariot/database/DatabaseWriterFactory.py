from typing import Dict, Type
from chariot.database.writer import DatabaseWriter, MongoDatabaseWriter, MySQLDatabaseWriter
from chariot.database.configuration import DatabaseConfiguration
from chariot.utility import AbstractFactory


class _DatabaseWriterFactory(AbstractFactory):
    def __init__(self):
        self.instanceMap: Dict[str, Type[DatabaseWriter]] = {
            'MongoDB': MongoDatabaseWriter,
            'MySQL': MySQLDatabaseWriter
        }
        self.instanceName: str = 'database'
        self.typeField: str = 'type'
    
    def getInstance(self, config: DatabaseConfiguration) -> DatabaseWriter:
        return super().getInstance(config)


# Return singleton
DatabaseWriterFactory = _DatabaseWriterFactory()

__all__ = ['DatabaseWriterFactory']
