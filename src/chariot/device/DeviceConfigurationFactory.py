from typing import Dict, Type
from chariot.device.configuration import DeviceConfiguration, ImpinjR420Configuration, ImpinjXArrayConfiguration
from chariot.utility import AbstractFactory
from chariot.utility.JSONTypes import JSONObject
from test.testutils import TestDeviceConfiguration


class _DeviceConfigurationFactory(AbstractFactory):
    def __init__(self):
        self.instanceMap: Dict[str, Type[DeviceConfiguration]] = {
            'ImpinjXArray': ImpinjXArrayConfiguration,
            'ImpinjSpeedwayR420': ImpinjR420Configuration,
            'TestDevice': TestDeviceConfiguration
        }
        self.typeField = 'deviceType'
        self.instanceName: str = 'device configuration'

    def getInstance(self, config: JSONObject) -> DeviceConfiguration:
        return super().getInstance(config)


# Return singleton
DeviceConfigurationFactory = _DeviceConfigurationFactory()

__all__ = ['DeviceConfigurationFactory']
