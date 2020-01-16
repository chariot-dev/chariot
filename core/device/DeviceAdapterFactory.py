from typing import Any, Dict
from json import load
from os import path

class DeviceAdapterFactory:
    def __init__(self):
        currentPath = path.dirname(path.abspath(__file__))
        with open(f'{currentPath}/drivers/supportedDevices.json') as deviceList:
            self.supportedDevices: Dict[str, Any] = load(deviceList)

    def getInstance(self, configMap: Dict[str, Any]):
        # configMap
        # deviceType: xxx
        # nickname: yyy
        # className: zzz
        if 'deviceType' not in configMap:
            # raise InvalidDeviceConfigurationError
            pass
        if configMap['deviceType'] not in self.supportedDevices:
            # raise UnsupportedDeviceError
            pass
