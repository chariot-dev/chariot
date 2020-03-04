from typing import Dict, Type
from chariot.device.configuration import DeviceConfiguration
from chariot.device.configuration import ImpinjR420Configuration
from chariot.device.configuration import ImpinjXArrayConfiguration
from chariot.utility import AbstractFactory
from chariot.utility.JSONTypes import JSONObject


class _DeviceConfigurationFactory(AbstractFactory):
    def __init__(self):
        self.instanceMap: Dict[str, Type[DeviceConfiguration]] = {
            'ImpinjXArray': ImpinjXArrayConfiguration,
            'ImpinjSpeedwayR420': ImpinjR420Configuration
        }
        self.typeField = 'deviceType'
        self.instanceName: str = 'device configuration'
    
    def getInstance(self, config: JSONObject) -> DeviceConfiguration:
        return super().getInstance(config)


# Return singleton 
DeviceConfigurationFactory = _DeviceConfigurationFactory()

__all__ = ['DeviceConfigurationFactory']
