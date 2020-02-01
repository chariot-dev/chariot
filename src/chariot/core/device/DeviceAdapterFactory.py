from typing import Dict, Type
from json import load
from os import path

from chariot.core.JSONTypes import JSONDict
from chariot.core.device.adapter.DeviceAdapter import DeviceAdapter
from chariot.core.device.configuration.DeviceConfiguration import DeviceConfiguration
from chariot.core.device.adapter.ImpinjR420Adapter import ImpinjR420Adapter
from chariot.core.device.adapter.ImpinjXArrayAdapter import ImpinjXArrayAdapter


class _DeviceAdapterFactory:
    def __init__(self):
        self.deviceMap: Dict[str, Type[DeviceAdapter]] = {
            'Impinj xArray': ImpinjXArrayAdapter,
            'Impinj Speedway R420': ImpinjR420Adapter
        }

        currentPath = path.dirname(path.abspath(__file__))
        with open(f'{currentPath}/driver/supportedDevices.json') as deviceList:
            self.__supportedDevices: JSONDict = load(deviceList)

    def getInstance(self, config: Type[DeviceConfiguration]) -> Type[DeviceAdapter]:
        if config.deviceType not in self.__supportedDevices:
            # raise UnsupportedDeviceError
            raise AssertionError

        instance: Type[DeviceAdapter] = self.deviceMap[config.deviceType](config)
        return instance

    def getsupportedDevices(self) -> JSONDict:
        return self.__supportedDevices


# return a singleton instance
DeviceAdapterFactory = _DeviceAdapterFactory()


__all__ = ['DeviceAdapterFactory']
