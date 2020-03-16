from typing import Dict, Type
from json import load
from os import path
from chariot.utility import AbstractFactory
from chariot.utility.JSONTypes import JSONDict
from chariot.device.adapter import DeviceAdapter, ImpinjR420Adapter, ImpinjXArrayAdapter, TestAdapter
from chariot.device.configuration import DeviceConfiguration
from chariot.utility.exceptions import ItemNotSupported, ErrorStrings


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
            raise ItemNotSupported(
                ErrorStrings.ERR_Generic_Device_Template.value.format("/device/drive/GenericRequiredFields.json")
            )

    def getInstance(self, config: DeviceConfiguration) -> DeviceAdapter:
        return super().getInstance(config)

    def getsupportedDevices(self) -> JSONDict:
        # update each device configuration with generic required fields
        fullDevices: Dict[str, DeviceConfiguration] = {}

        for device in self.instanceMap.keys():
            fullDevices.update(self.getSpecifiedDeviceTemplate(device))
        return fullDevices

    def getDeviceInformation(self, deviceName: str) -> JSONDict:
        if deviceName not in self._supportedDevices:
            raise ItemNotSupported(ErrorStrings.ERR_Item_Not_Supported.value.format(self.instanceName, deviceName))
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
            raise ItemNotSupported(ErrorStrings.ERR_Item_Not_Supported.value.format(self.instanceName, deviceName))

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
