from typing import Dict, Type
from chariot.device.configuration.DeviceConfiguration import DeviceConfiguration
from chariot.device.configuration.ImpinjR420Configuration import ImpinjR420Configuration
from chariot.device.configuration.ImpinjXArrayConfiguration import ImpinjXArrayConfiguration
from chariot.device.configuration.TestConfiguration import TestConfiguration
from chariot.utility.AbstractFactory import AbstractFactory
from chariot.utility.JSONTypes import JSONObject


class _DeviceConfigurationFactory(AbstractFactory):
    def __init__(self):
        self.instanceMap: Dict[str, Type[DeviceConfiguration]] = {
            'ImpinjXArray': ImpinjXArrayConfiguration,
            'ImpinjSpeedwayR420': ImpinjR420Configuration,
            'TestDevice': TestConfiguration
        }
        self.typeField = 'deviceType'
        self.instanceName: str = 'device configuration'

    def getInstance(self, config: JSONObject) -> DeviceConfiguration:
        return super().getInstance(config)


# Return singleton
DeviceConfigurationFactory = _DeviceConfigurationFactory()

__all__ = ['DeviceConfigurationFactory']
