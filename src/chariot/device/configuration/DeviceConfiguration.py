from chariot.configuration.Configuration import Configuration
from chariot.utility.JSONTypes import JSONDict, JSONObject
from typing import Dict, Type


class DeviceConfiguration(Configuration):
    requiredFields: Dict[str, Type[JSONObject]] = {
        'deviceId': str,
        'deviceType': str,
        'pollDelay': int,
    }

    def _validateSubsetConfig(self, newConfig: JSONDict) -> None:
        for field in newConfig:
            if field == 'deviceType':
                # cannot edit deviceType
                raise AssertionError
        super()._validateSubsetConfig(newConfig)

    def getId(self) -> str:
        return getattr(self, 'deviceId')

    def getIdField(self) -> str:
        return 'deviceId'


__all__ = ['DeviceConfiguration']
