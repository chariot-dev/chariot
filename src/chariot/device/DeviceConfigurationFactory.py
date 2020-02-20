from typing import Dict, Type
from chariot.device.configuration.DeviceConfiguration import DeviceConfiguration
from chariot.device.configuration.ImpinjR420Configuration import ImpinjR420Configuration
from chariot.device.configuration.ImpinjXArrayConfiguration import ImpinjXArrayConfiguration
from chariot.utility.AbstractFactory import AbstractFactory


class _DeviceConfigurationFactory(AbstractFactory):
    def __init__(self):
        self.instanceMap: Dict[str, Type[DeviceConfiguration]] = {
            'Impinj xArray': ImpinjXArrayConfiguration,
            'Impinj Speedway R420': ImpinjR420Configuration
        }
        self.instanceName: str = 'device configuration'


# Return singleton 
DeviceConfigurationFactory = _DeviceConfigurationFactory()

__all__ = ['DeviceConfigurationFactory']
