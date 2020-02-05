from typing import Dict, List, Type

from chariot.JSONTypes import JSONDict, JSONObject
from chariot.device.configuration.DeviceConfiguration import DeviceConfiguration


class ImpinjXArrayConfiguration(DeviceConfiguration):
    def __init__(self, configMap: JSONDict):
        super().__init__(configMap)

    def _validateConfig(self, configMap: JSONDict) -> None:
        super()._validateConfig(configMap)
        if configMap['deviceType'] != 'Impinj xArray':
            raise AssertionError

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

        for field, fieldType in requiredFields:
            if field not in configMap or not isinstance(
                    configMap[field], fieldType):
                raise ValueError

        for field, fieldType in optionalFields:
            if field in configMap and not isinstance(
                    configMap[field], fieldType):
                raise ValueError


__all__ = ['ImpinjXArrayConfiguration']
