from abc import ABC
from typing import Dict, Type
from json import dumps

from chariot.core.JSONTypes import JSONDict, JSONObject


class DeviceConfiguration(ABC):
    def __init__(self, configMap: JSONDict):
        self._validateConfig(configMap)
        self.deviceId: str = configMap['id']
        self.deviceType: str = configMap['deviceType']
        self.nickname: str = configMap['nickname']

    def _validateConfig(self, configMap: JSONDict) -> None:
        fields: Dict[str, Type[JSONObject]] = {
            'id': str, 'deviceType': str, 'nickname': str}
        for field in fields:
            if field not in configMap or not isinstance(
                    configMap[field], fields[field]):
                raise ValueError

    def __str__(self):
        output: JSONDict = {}
        output['id'] = self.deviceId
        output['deviceType'] = self.deviceType
        output['nickname'] = self.nickname
        return dumps(output)

    def toJSON(self) -> str:
        return self.__str__()


__all__ = ['DeviceConfiguration']
