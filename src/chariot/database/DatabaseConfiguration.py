import abc
from json import dumps
from typing import Dict, Type

from chariot.utility.JSONTypes import JSONDict, JSONObject


class DatabaseConfiguration(metaclass=abc.ABCMeta):
    requiredFields: Dict[str, Type[JSONObject]] = {
        'host': str,
        'port': int,
        'databaseType': str
    }

    optionalFields: Dict[str, Type[JSONObject]] = {}

    def __init__(self, configMap: JSONDict):
        self._validateInitialConfig(configMap)
        for key, value in configMap.items():
            setattr(self, key, value)

    def __str__(self):
        output: JSONDict = dict(self)
        return dumps(output)

    def __iter__(self):
        for key in self.requiredFields:
            yield(key, getattr(self, key))
        for key in self.optionalFields:
            if hasattr(self, key):
                yield(key, getattr(self, key))

    def _isValidField(self, field: str) -> bool:
        if field not in self.requiredFields and field not in self.optionalFields:
            return False
        else:
            return True
        # return field not in self.requiredFields and field not in
        # self.optionalFields

    def _validateInitialConfig(self, configMap: JSONDict) -> None:
        for field in configMap:
            if not self._isValidField(field):
                raise AssertionError("Invalid field '" + field + "'")

        for field, fieldType in self.requiredFields.items():
            if field not in configMap or not isinstance(
                    configMap[field], fieldType):
                raise ValueError(
                    "Config field '" +
                    field +
                    "' is missing or invalid")

        for field, fieldType in self.optionalFields.items():
            if field in configMap and not isinstance(
                    configMap[field], fieldType):
                raise ValueError(
                    "Config field '" +
                    field +
                    "' is invalid")

    def _validateSubsetConfig(self, newConfig: JSONDict) -> None:
        for field, value in newConfig.items():
            if not self._isValidField(field):
                raise AssertionError("Invalid field '" + field + "'")
            if field in self.optionalFields:
                if not isinstance(value, self.optionalFields[field]):
                    raise ValueError(
                        "Config field '" +
                        field +
                        "' is invalid")
            elif field in self.requiredFields:
                if field == 'databaseType':
                    raise AssertionError("Database type cannot be modified")
                if not isinstance(value, self.requiredFields[field]):
                    raise ValueError(
                        "Config field '" +
                        field +
                        "' is invalid")

    def modifyConfig(self, newConfig: JSONDict) -> None:
        self._validateSubsetConfig(newConfig)
        for key, value in newConfig.items():
            setattr(self, key, value)

    def toJSON(self) -> str:
        return self.__str__()
