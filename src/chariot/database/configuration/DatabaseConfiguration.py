from chariot.configuration.Configuration import Configuration
from chariot.utility.JSONTypes import JSONDict, JSONObject
from json import dumps
from typing import Dict, Type


class DatabaseConfiguration(Configuration):
    requiredFields: Dict[str, Type[JSONObject]] = {
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


__all__ = ['DatabaseConfiguration']
