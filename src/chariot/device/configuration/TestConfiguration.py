from typing import Dict, List, Type
from chariot.utility.JSONTypes import JSONDict, JSONObject
from chariot.device.configuration.DeviceConfiguration import DeviceConfiguration

class TestConfiguration(DeviceConfiguration):
    requiredFields: Dict[str, Type[JSONObject]] = {
        'buffSize': int,
    }
    optionalFields: Dict[str, Type[JSONObject]] = {
        'seedVal': int,
    }

    def __init__(self, configMap: JSONDict):
        self.requiredFields.update(super().requiredFields)
        self.optionalFields.update(super().optionalFields)
        super().__init__(configMap)

    def _validateInitialConfig(self, configMap: JSONDict) -> None:
        super()._validateInitialConfig(configMap)
        if configMap['deviceType'] != 'Test Device':
            raise AssertionError

__all__ = ['TestConfiguration']
