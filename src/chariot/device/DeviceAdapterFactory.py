from typing import Dict, Type
from json import load
from os import path
from chariot.utility.AbstractFactory import AbstractFactory
from chariot.utility.JSONTypes import JSONDict
from chariot.device.adapter.DeviceAdapter import DeviceAdapter
from chariot.device.configuration.DeviceConfiguration import DeviceConfiguration
from chariot.device.adapter.ImpinjR420Adapter import ImpinjR420Adapter
from chariot.device.adapter.ImpinjXArrayAdapter import ImpinjXArrayAdapter
from chariot.device.adapter.TestAdapter import TestAdapter
from chariot.utility.exceptions.CustomExceptions import DeviceNotSupported
from chariot.utility.exceptions.ErrorStrings import ErrorStrings

class _DeviceAdapterFactory(AbstractFactory):
    def __init__(self):
        self.instanceMap: Dict[str, Type[DeviceAdapter]] = {
            'ImpinjXArray': ImpinjXArrayAdapter,
            'ImpinjSpeedwayR420': ImpinjR420Adapter,
            'TestDevice': TestAdapter,
        }
        self.instanceName: str = 'device'
        self.typeField: str = 'deviceType'

        currentPath = path.dirname(path.abspath(__file__))
        with open(f'{currentPath}/driver/supportedDevices.json') as deviceList:
            self._supportedDevices: JSONDict = load(deviceList)

        try:
            with open(f'{currentPath}/driver/GenericRequiredFields.json') as genericTemplate:
                self._genericRequiredTemplate = load(genericTemplate)
        except IOError:
            raise DeviceNotSupported(ErrorStrings.ERR_Generic_Device_Template.value)

    def getInstance(self, config: DeviceConfiguration) -> DeviceAdapter:
        return super().getInstance(config)

    def getsupportedDevices(self) -> JSONDict:
        return self._supportedDevices

    def getDeviceInformation(self, deviceName: str) -> JSONDict:
        if deviceName not in self._supportedDevices:
            raise DeviceNotSupported(ErrorStrings.ERR_Device_Not_Supported.value.format(deviceName))
        return self._supportedDevices[deviceName]

    # this method returns a specified device json file
    def getSpecifiedDeviceTemplate(self, deviceName) -> JSONDict:
        # build path to json file
        currentPath = path.dirname(path.abspath(__file__))
        try:
            with open(f'{currentPath}/driver/{deviceName}.json') as deviceTemplate:
                # now combine the specified device template with that of the generic template
                specificDevice = load(deviceTemplate)
                return self.combineConfigWithGeneric(specificDevice, deviceName)
        except:
            raise DeviceNotSupported(ErrorStrings.ERR_Device_Not_Supported.value.format(deviceName))

    # use this method to combine settings from a specific configuration instance with the generic required fields
    def combineConfigWithGeneric(self, config: JSONDict, deviceType: str):
        combinedDict = config

        # combine settings of the config with the generic required fields
        for field in self._genericRequiredTemplate["settings"]:
            combinedDict[deviceType]["settings"].insert(0, field)  # add required field add beginning of list

        return combinedDict


# return a singleton instance
DeviceAdapterFactory = _DeviceAdapterFactory()

__all__ = ['DeviceAdapterFactory']
