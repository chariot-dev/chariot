from chariot.configuration import Configuration
from chariot.utility.JSONTypes import JSONDict, JSONObject
from typing import Dict, Type


class DatabaseConfiguration(Configuration):
    requiredFields: Dict[str, Type[JSONObject]] = {
        'dbId': str,
        'databaseName': str,
        'type': str,
        'host': str,
    }

    optionalFields: Dict[str, Type[JSONObject]] = {
        'port': int,
        'tableName': str,
        'timeoutMS': int
    }

    def __init__(self, configMap):
        super().__init__(configMap)
        if not hasattr(self, 'tableName'):
            setattr(self, 'tableName', 'data')
        if not hasattr(self, 'timeoutMS'):
            setattr(self, 'timeoutMS', 5000)

    def _validateSubsetConfig(self, newConfig: JSONDict) -> None:
        super()._validateSubsetConfig(newConfig)
        for field in newConfig:
            if field == 'type':
                # cannot edit databaseType
                raise AssertionError

    def getId(self) -> str:
        return getattr(self, 'dbId')

    def getIdField(self) -> str:
        return 'dbId'


__all__ = ['DatabaseConfiguration']
