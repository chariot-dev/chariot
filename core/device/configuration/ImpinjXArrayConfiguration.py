from typing import Dict, List, Type
from core.JSONTypes import JSONDict, JSONObject
from core.device.configuration.DeviceConfiguration import DeviceConfiguration


class ImpinjXArrayConfiguration(DeviceConfiguration):
    requiredFields: Dict[str, Type[JSONObject]] = {
        'ipAddress': str,
        'authUsername': str,
        'authPassword': str,
    }
    optionalFields: Dict[str, Type[JSONObject]] = {
        'jobName': str,
        'facility': str,
        'startDelay': str,
        'readerGroups': List[str],
        'reportToDatabaseEnabled': bool,
        'reportToHistoryEnabled': bool,
        'reportToMessageQueueEnabled': bool,
        'useOtherJobData': bool,
    }

    def __init__(self, configMap: JSONDict):
        self.requiredFields.update(super().requiredFields)
        self.optionalFields.update(super().optionalFields)
        super().__init__(configMap)

    def _validateConfig(self, configMap: JSONDict) -> None:
        super()._validateConfig(configMap)
        if configMap['deviceType'] != 'Impinj xArray':
            raise AssertionError


__all__ = ['ImpinjXArrayConfiguration']
