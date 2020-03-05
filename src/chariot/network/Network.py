from typing import Dict, List, Type
from chariot.device.adapter.DeviceAdapter import DeviceAdapter
from chariot.utility.exceptions.CustomExceptions import NameNotFoundError, NoIdentifierError, DuplicateNameError
from chariot.utility.exceptions.ErrorStrings import ErrorStrings
from chariot.network.configuration.NetworkConfiguration import NetworkConfiguration
from chariot.utility.JSONTypes import JSONDict
from chariot.utility.Manager import Manager


class Network(Manager):

    def __init__(self, config: Type[NetworkConfiguration]):
        self._config: Type[NetworkConfiguration] = config
        self.collection: Dict[str, DeviceAdapter] = {}

    def getNetworkName(self) -> str:
        return self._config.networkName

    def getDescription(self) -> str:
        return self._config.description

    def updateConfig(self, config: JSONDict):
        self._config.modifyConfig(config)

    def getConfiguration(self) -> NetworkConfiguration:
        return self._config

    def addDevice(self, device: DeviceAdapter):
        self._addToCollection(device)
        
    def deleteDevice(self, deviceId: str):
        self._deleteFromCollection(deviceId)

    def getDevice(self, deviceId: str) -> DeviceAdapter:
        return self._retrieveFromCollection(deviceId)

    # This method gives a new device name to an already defined device in the collection
    def replaceDevice(self, newName: str, toFind: str):
        self._modifyNameInCollection(newName, toFind)

    def getDeviceNames(self) -> List[str]:
        devices: List[str] = []

        for deviceName in self.collection:
            devices.append(deviceName)

        return devices

    def toDict(self):
        network: Dict[str, str] = {'NetworkName': self._config.networkName, 'Description': self._config.description}

        # add each deviceId as key and the configuration as value
        for key in self.collection:
            network[key] = self.getDevice(key).getConfiguration().toDict()

        return network

    # importDeviceConfig
    # exportNetwork - again seems like a utility method
    # saveNetwork - idea is to save this network configuration to the UserAccount
