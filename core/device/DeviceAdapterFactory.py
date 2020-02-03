from typing import Dict, Type
from json import load
from os import path
from core.JSONTypes import JSONDict
from core.device.adapter.DeviceAdapter import DeviceAdapter
from core.device.configuration.DeviceConfiguration import DeviceConfiguration
from core.device.adapter.ImpinjR420Adapter import ImpinjR420Adapter
from core.device.adapter.ImpinjXArrayAdapter import ImpinjXArrayAdapter


class _DeviceAdapterFactory:
    def __init__(self):
        self.deviceMap: Dict[str, Type[DeviceAdapter]] = {
            'Impinj xArray': ImpinjXArrayAdapter,
            'Impinj Speedway R420': ImpinjR420Adapter
        }

        currentPath = path.dirname(path.abspath(__file__))
        with open(f'{currentPath}/driver/supportedDevices.json') as deviceList:
            self._supportedDevices: JSONDict = load(deviceList)

    def getInstance(self, config: Type[DeviceConfiguration]) -> Type[DeviceAdapter]:
        if config.deviceType not in self._supportedDevices:
            # raise UnsupportedDeviceError
            raise AssertionError

        instance: Type[DeviceAdapter] = self.deviceMap[config.deviceType](config)
        return instance

    def getsupportedDevices(self) -> JSONDict:
        return self._supportedDevices

    def getDeviceInformation(self, deviceName: str) -> JSONDict:
        if deviceName not in self._supportedDevices:
            # raise UnsupportedDeviceError
            raise AssertionError
        return self._supportedDevices[deviceName]


# return a singleton instance
DeviceAdapterFactory = _DeviceAdapterFactory()


__all__ = ['DeviceAdapterFactory']
