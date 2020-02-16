import abc
from json import dumps
from typing import Dict, Type

from chariot.JSONTypes import JSONDict


class DatabaseConfiguration(metaclass=abc.ABCMeta):
    def __init__(self, configMap: JSONDict):
        self.validateConfig(configMap)
        self.configMap: JSONDict = configMap

    def validateConfig(self, configMap: JSONDict):
        fields: Dict[str, Type[JSONObject]] = {
            'host': str, 'port': int, 'databaseType': str
        }
        for field in fields:
            if field not in configMap or not isinstance(
                configMap[field], fields[field]
            ):
                raise ValueError

    def __str__(self) -> str:
        return dumps(self.configMap)

    def toJSON(self) -> str:
        return self.__str__()
