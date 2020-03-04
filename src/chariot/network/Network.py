from typing import Dict, List, Type
from chariot.device.adapter.DeviceAdapter import DeviceAdapter
from chariot.utility.exceptions.CustomExceptions import NameNotFoundError, NoIdentifierError, DuplicateNameError
from chariot.utility.exceptions.ErrorStrings import ErrorStrings
from chariot.network.configuration.NetworkConfiguration import NetworkConfiguration
from chariot.utility.JSONTypes import JSONDict


class Network:

    def __init__(self, config: Type[NetworkConfiguration]):
        self._config: Type[NetworkConfiguration] = config
        self.devices: Dict[str, DeviceAdapter] = {}

    def getNetworkName(self) -> str:
        return self._config.networkName

    def getDescription(self) -> str:
        return self._config.description

    def modifyConfiguration(self, config: JSONDict):
        try:
            self._config.modifyConfig(config)
        except Exception as e:
            raise e

    def getConfiguration(self) -> NetworkConfiguration:
        return self._config

    # figure out how much error-checking to do
    def addDevice(self, device: DeviceAdapter):
        if device is None:
            NoIdentifierError(ErrorStrings.ERR_Specify_Device_Identifier)

        # Currently just restricting adding a device that already exists in collection
        if self.isDeviceNameUnique(device.getId()):
            # name is unique, safely add to dict
            self.devices[device.getId()] = device
        else:
            raise DuplicateNameError(
                ErrorStrings.ERR_Not_Unique_Device_Name.value.format(device.getId(), self.getNetworkName()))

    def getDeviceByDeviceName(self, nameToFind: str) -> DeviceAdapter:
        if nameToFind is None:
            NoIdentifierError(ErrorStrings.ERR_Specify_Device_Identifier)

        if nameToFind in self.devices:
            return self.devices[nameToFind]
        else:
            raise NameNotFoundError(
                ErrorStrings.ERR_Device_Not_Found_In_Collection.value.format(nameToFind, self.getNetworkName()))

    def deleteDeviceByName(self, deviceName: str):
        if deviceName in self.devices:
            del self.devices[deviceName]
        else:
            raise NameNotFoundError(
                ErrorStrings.ERR_Device_Not_Found_In_Collection.value.format(deviceName, self.getNetworkName()))

    def isDeviceNameUnique(self, name) -> bool:
        isUnique: bool = True
        if name in self.devices:
            isUnique = False

        return isUnique

    def getDeviceNames(self) -> List[str]:
        devices: List[str] = []

        for deviceName in self.devices:
            devices.append(deviceName)

        return devices

    def toDict(self):
        network: Dict[str, str] = {'NetworkName': self._config.networkName, 'Description': self._config.description}

        # add each deviceId as key and the configuration as value
        for key in self.devices:
            network[key] = self.getDeviceByDeviceName(key).getDeviceConfiguration().toDict()

        return network

    # This method gives a new device name to an already defined device
    def modifyDeviceNameByName(self, newName: str, toFind: str):
        # check that newName is unique to avoid data overwrites
        if not self.isDeviceNameUnique(newName):
            raise DuplicateNameError(
                ErrorStrings.ERR_Not_Unique_Network_Name.value.format(newName)
            )

        device: DeviceAdapter = self.getDeviceByDeviceName(toFind)

        # update device name
        device.setId(newName)

        # update collection, make new key and delete the old one
        self.devices[newName] = self.devices[toFind]
        del self.devices[toFind]

    # importDeviceConfig
    # exportNetwork - again seems like a utility method
    # saveNetwork - idea is to save this network configuration to the UserAccount
    # modifyDevice - need to figure out how to be able to do this for each device, given that each one
    # has different variables
