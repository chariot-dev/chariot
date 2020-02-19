from chariot.configuration.Configuration import Configuration
from chariot.utility.JSONTypes import JSONDict, JSONObject
from json import dumps
from typing import Dict, Type

class DatabaseConfiguration(Configuration):
    requiredFields: Dict[str, Type[JSONObject]] = {
        'databaseType': str
    }

    def _validateSubsetConfig(self, newConfig: JSONDict) -> None:
        super()._validateSubsetConfig(newConfig)
        for field in newConfig:
            if field == 'databaseType':
                # cannot edit databaseType
                raise AssertionError


__all__ = ['DatabaseConfiguration']
