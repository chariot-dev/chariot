from typing import Dict, List, Type
from chariot.utility.JSONTypes import JSONDict, JSONObject
from chariot.device.configuration.DeviceConfiguration import DeviceConfiguration


class ImpinjR420Configuration(DeviceConfiguration):
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
        'EnableROSpecID': bool,
        'EnableSpecIndex': bool,
        'EnableInventoryParameterSpecID': bool,
        'EnableAntennaID': bool,
        'EnableChannelIndex': bool,
        'EnablePeakRSSI_General': bool,
        'EnableFirstSeenTimestamp': bool,
        'EnableTagSeenCount': bool,
        'EnableAccessSpecID': bool,
        'EnablePeakRSSI_Impinj': bool,
        'EnableRFPhaseAngle': bool,
        'EnableRFDopplerFrequency': bool,
    }

    def __init__(self, configMap: JSONDict):
        self.requiredFields.update(super().requiredFields)
        self.optionalFields.update(super().optionalFields)
        super().__init__(self._flattenSettingsGroups(configMap))

    def _flattenSettingsGroups(self, configMap: JSONDict) -> JSONDict:
        # since some R420 settings come in as a group, we need to flatten them to make verification easier
        for _, entry in configMap.items():
            if isinstance(entry, JSONDict):
                for key, value in entry.items():
                    configMap[key] = value
        return configMap

    def _validateInitialConfig(self, configMap: JSONDict) -> None:
        super()._validateInitialConfig(configMap)
        if configMap['deviceType'] != 'Impinj Speedway R420':
            raise AssertionError


__all__ = ['ImpinjR420Configuration']
