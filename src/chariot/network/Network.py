from typing import Dict

from chariot.device.adapter.DeviceAdapter import DeviceAdapter
from chariot.utility.exceptions.DuplicateNameError import DuplicateNameError
from chariot.utility.exceptions.NameNotFoundError import NameNotFoundError


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
        if not device:
            pass
            # need custom exception

        # Currently just restricting adding a device that already exists in collection
        if self.isDeviceNameUnique(device.getDeviceName()):
            # name is unique, safely add to dict
            self.devices[device.getDeviceName] = device
        else:
            raise DuplicateNameError(device.getDeviceName)

    def getDeviceByDeviceName(self, nameToFind: str) -> DeviceAdapter:
        if nameToFind in self.devices:
            return self.devices[nameToFind]
        else:
            raise NameNotFoundError('device', nameToFind, self.networkName)

    def deleteDeviceByName(self, deviceName: str):
        if deviceName in self.devices:
            del self.devices[deviceName]
        else:
            raise NameNotFoundError('device', deviceName, self.networkName)

    def isDeviceNameUnique(self, name) -> bool:
        isUnique: bool = True
        if name in self.devices:
            isUnique = False

        return isUnique

    def toString(self):
        network: Dict[str, str] = {self.networkName: self.networkDesc}
        for key in self.devices:
            network[key] = self.getDeviceByDeviceName(key).config

        return network

    # importDeviceConfig
    # exportNetwork - again seems like a utility method
    # saveNetwork - idea is to save this network configuration to the UserAccount
    # modifyDevice - need to figure out how to be able to do this for each device, given that each one
    # has different variables
