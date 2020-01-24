from typing import Dict, List, Type
from core.JSONTypes import JSONDict, JSONObject
from core.device.configuration.DeviceConfiguration import DeviceConfiguration


class ImpinjR420Configuration(DeviceConfiguration):
    def __init__(self, configMap: JSONDict):
        super().__init__(self._flattenSettingsGroups(configMap))

    def _flattenSettingsGroups(self, configMap: JSONDict) -> JSONDict:
        # since some R420 settings come in as a group, we need to flatten them to make verification easier
        for _, entry in configMap:
            if isinstance(entry, JSONDict):
                for key, value in entry:
                    configMap[key] = value
        return configMap

    def _validateConfig(self, configMap: JSONDict) -> None:
        super()._validateConfig(configMap)
        if configMap['deviceType'] != 'Impinj Speedway R420':
            raise AssertionError

        requiredFields: Dict[str, Type[JSONObject]] = {
            'ipAddress': str,
            'tag_population': int,
        }
        optionalFields: Dict[str, Type[JSONObject]] = {
            'antennas': List[int],
            'report_every_n_tags': int,
            'tx_power': int,
            'session': int,
            'start_inventory': bool,
            'mode_identifier': bool,
            'reportToMessageQueueEnabled': bool,
            'useOtherJobData': bool,
        }

        for field, fieldType in requiredFields:
            if not field in configMap or not isinstance(configMap[field], fieldType):
                raise ValueError

        for field, fieldType in optionalFields:
            if field in configMap and not isinstance(configMap[field], fieldType):
                raise ValueError


__all__ = ['ImpinjR420Configuration']
