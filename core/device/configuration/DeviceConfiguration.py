from abc import ABC
from typing import Dict, Type
from json import dumps
from core.JSONTypes import JSONDict, JSONObject


class DeviceConfiguration(ABC):
    requiredFields: Dict[str, Type[JSONObject]] = {
        'deviceId': str,
        'deviceType': str,
        'nickname': str,
    }
    optionalFields: Dict[str, Type[JSONObject]] = {}

    def __init__(self, configMap: JSONDict):
        self._validateConfig(configMap)
        for key, value in configMap:
            setattr(self, key, value)

    def __iter__(self):
        for key in self.requiredFields:
            yield(key, getattr(self, key))
        for key in self.optionalFields:
            yield(key, getattr(self, key))

    def __str__(self):
        output: JSONDict = dict(self)
        return dumps(output)
    
    def _validateConfig(self, configMap: JSONDict) -> None:
        for field in configMap:
            if not field in self.requiredFields and not field in self.optionalFields:
                raise AssertionError

        for field, fieldType in self.requiredFields:
            if not field in configMap or not isinstance(configMap[field], fieldType):
                raise ValueError
        
        for field, fieldType in self.optionalFields:
            if field in configMap and not isinstance(configMap[field], fieldType):
                raise ValueError

    def toJSON(self) -> str:
        return self.__str__()

    def toDict(self) -> JSONDict:
        return dict(self)


__all__ = ['DeviceConfiguration']
