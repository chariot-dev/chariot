from typing import Dict

from chariot.device.adapter.DeviceAdapter import DeviceAdapter
from chariot.utility.exceptions.DuplicateNameError import DuplicateNameError
from chariot.utility.exceptions.NameNotFoundError import NameNotFoundError
from chariot.utility.exceptions.NoIdentifierError import NoIdentifierError
from chariot.utility.exceptions.ErrorStrings import ErrorStrings


class Network:

    def __init__(self, networkName: str, networkDesc: str):
        self.networkName = networkName
        self.networkDesc = networkDesc
        self.devices: Dict[str, DeviceAdapter] = {}

    def modifyNetworkName(self, newName: str):
        self.networkName = newName

    def modifyNetworkDesc(self, newDesc: str):
        self.networkDesc = newDesc

    def getNetworkName(self) -> str:
        return self.networkName

    def getNetworkDesc(self) -> str:
        return self.networkDesc

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

    def toString(self):
        network: Dict[str, str] = {'NetworkName': self.networkName, 'Description': self.networkDesc}

        # add each deviceId as key and the configuration as value
        for key in self.devices:
            network[key] = self.getDeviceByDeviceName(key).getDeviceConfiguration()

        return network

    # importDeviceConfig
    # exportNetwork - again seems like a utility method
    # saveNetwork - idea is to save this network configuration to the UserAccount
    # modifyDevice - need to figure out how to be able to do this for each device, given that each one
    # has different variables
