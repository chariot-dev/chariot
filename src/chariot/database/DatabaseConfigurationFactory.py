from typing import Dict, Type
from chariot.database.configuration import DatabaseConfiguration
from chariot.database.configuration import MongoDatabaseConfiguration
from chariot.database.configuration import MySQLDatabaseConfiguration
from chariot.utility import AbstractFactory
from chariot.utility.JSONTypes import JSONObject


class _DatabaseConfigurationFactory(AbstractFactory):
    def __init__(self):
        self.instanceMap: Dict[str, Type[DatabaseConfiguration]] = {
            'MongoDB': MongoDatabaseConfiguration,
            'MySQL': MySQLDatabaseConfiguration
        }
        self.typeField = 'type'
        self.instanceName: str = 'database configuration'

    def getInstance(self, config: JSONObject) -> DatabaseConfiguration:
        return super().getInstance(config)


# Return singleton 
DatabaseConfigurationFactory = _DatabaseConfigurationFactory()

__all__ = ['DatabaseConfigurationFactory']
