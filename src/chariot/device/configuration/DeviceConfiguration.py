from chariot.configuration.Configuration import Configuration
from chariot.utility.JSONTypes import JSONDict, JSONObject
from json import dumps
from typing import Dict, Type

class DeviceConfiguration(Configuration):
    requiredFields: Dict[str, Type[JSONObject]] = {
        'deviceId': str,
        'deviceType': str,
        'pollDelay': str,
    }

    def _validateSubsetConfig(self, newConfig: JSONDict) -> None:
        for field in newConfig:
            if field == 'deviceType':
                # cannot edit deviceType
                raise AssertionError
        super()._validateSubsetConfig(newConfig)


__all__ = ['DeviceConfiguration']
