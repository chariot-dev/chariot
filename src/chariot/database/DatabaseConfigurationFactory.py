from typing import Dict, Type
from chariot.database.configuration.DatabaseConfiguration import DatabaseConfiguration
from chariot.database.configuration.MongoDatabaseConfiguration import MongoDatabaseConfiguration
from chariot.database.configuration.MySQLDatabaseConfiguration import MySQLDatabaseConfiguration
from chariot.utility.AbstractFactory import AbstractFactory


class _DatabaseConfigurationFactory(AbstractFactory):
    def __init__(self):
        self.instanceMap: Dict[str, Type[DatabaseConfiguration]] = {
            'MongoDB': MongoDatabaseConfiguration,
            'MySQL': MySQLDatabaseConfiguration
        }
        self.instanceName: str = 'database configuration'


# Return singleton 
DatabaseConfigurationFactory = _DatabaseConfigurationFactory()

__all__ = ['DatabaseConfigurationFactory']
