from typing import Dict, Type
from json import load
from os import path
from chariot.JSONTypes import JSONDict
from chariot.device.adapter.DeviceAdapter import DeviceAdapter
from chariot.device.configuration.DeviceConfiguration import DeviceConfiguration
from chariot.device.adapter.ImpinjR420Adapter import ImpinjR420Adapter
from chariot.device.adapter.ImpinjXArrayAdapter import ImpinjXArrayAdapter


class _DeviceAdapterFactory:
    def __init__(self):
        self.deviceMap: Dict[str, Type[DeviceAdapter]] = {
            'ImpinjxArray': ImpinjXArrayAdapter,
            'ImpinjSpeedwayR420': ImpinjR420Adapter
        }

        currentPath = path.dirname(path.abspath(__file__))
        with open(f'{currentPath}/driver/supportedDevices.json') as deviceList:
            self._supportedDevices: JSONDict = load(deviceList)

    def getInstance(self, config: Type[DeviceConfiguration]) -> Type[DeviceAdapter]:
        if config['deviceType'] not in self._supportedDevices:
            # raise UnsupportedDeviceError
            raise AssertionError

        instance: Type[DeviceAdapter] = self.deviceMap[config['deviceType']](config)
        return instance

    def getsupportedDevices(self) -> JSONDict:
        return self._supportedDevices

    def getDeviceInformation(self, deviceName: str) -> JSONDict:
        if deviceName not in self._supportedDevices:
            # raise UnsupportedDeviceError
            raise AssertionError
        return self._supportedDevices[deviceName]

    # this method returns a specified device json file
    def getSpecifiedDeviceTemplate(self, deviceName) -> JSONDict:
        #build path to json file
        currentPath = path.dirname(path.abspath(__file__))
        try:
            with open(f'{currentPath}/driver/{deviceName}.json') as deviceTemplate:
                return load(deviceTemplate)
        except:
            # make custom exception for device not supported
            pass


# return a singleton instance
DeviceAdapterFactory = _DeviceAdapterFactory()

__all__ = ['DeviceAdapterFactory']
