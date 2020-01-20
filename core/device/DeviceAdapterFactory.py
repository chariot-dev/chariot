from typing import Dict
from json import load
from os import path
from core.device import ConfigObject
from core.device.DeviceAdapter import DeviceAdapter


class DeviceAdapterFactory:
    def __init__(self):
        currentPath = path.dirname(path.abspath(__file__))
        with open(f'{currentPath}/drivers/supportedDevices.json') as deviceList:
            self.supportedDevices: ConfigObject = load(deviceList)

    def createInstance(self, configMap: ConfigObject) -> DeviceAdapter:
        pass

    def getInstance(self, configMap: ConfigObject) -> DeviceAdapter:        
        if 'deviceType' not in configMap:
            # raise InvalidDeviceConfigurationError
            pass
 
        if configMap['deviceType'] not in self.supportedDevices:
            # raise UnsupportedDeviceError
            pass

        # this is the condition for adding a new device 
        # any other device would have already had a nickname
        
        if configMap['nickname'] not in self.supportedDevices:
            device: DeviceAdapter = self.createInstance(configMap)


__all__ = ['DeviceAdapterFactory']
  