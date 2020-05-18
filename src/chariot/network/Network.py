from threading import Lock
from typing import Dict, List, Optional
from chariot.device.adapter import DeviceAdapter
from chariot.network.configuration.NetworkConfiguration import NetworkConfiguration
from chariot.utility.JSONTypes import JSONObject
from chariot.utility import Manager


class Network(Manager):
    def __init__(self, config: NetworkConfiguration):
        self._config: NetworkConfiguration = config
        self.collection: Dict[str, DeviceAdapter] = {}
        self._modLock: Optional[Lock] = None
        self._lockReason: Optional[str] = None

    def getDevices(self) -> Dict[str, DeviceAdapter]:
        return self.collection

    def getNetworkName(self) -> str:
        return self._config.networkName

    def getDescription(self) -> str:
        return self._config.description

    def getConfiguration(self) -> NetworkConfiguration:
        return self._config

    def addDevice(self, device: DeviceAdapter):
        self._addToCollection(device)

    def deleteDevice(self, deviceId: str):
        self._deleteFromCollection(deviceId)

    def getDevice(self, deviceId: str) -> DeviceAdapter:
        return self._retrieveFromCollection(deviceId)

    # This method gives a new device name to an already defined device in the collection
    def replaceDevice(self, toFind: str, newName: str):
        self._modifyNameInCollection(toFind, newName)

    def getDeviceNames(self) -> List[str]:
        devices: List[str] = []

        for deviceName in self.collection:
            devices.append(deviceName)

        return devices

    # this method locks the network from modification e.g during a collection episode for as long as the lock
    # passed in is active
    def lock(self, lock: Lock, reason: Optional[str] = None):
        if self._modLock is not None:
            raise AssertionError('The network was already locked')
        self._modLock = lock
        self._lockReason = reason

    def toDict(self):
        network: Dict[str, str] = self._config.toDict()

        # add each deviceId as key and the configuration as value
        # TODO: devices should be under a nested dict 'devices'
        for key, device in self.collection.items():
            network[key] = device.toDict()

        return network

    def updateConfig(self, config: JSONObject) -> None:
        # if there is a modification lock in place and it is locked,
        if self._modLock and self._modLock.locked():
            message: str = 'This network is currently locked from modification'
            if self._lockReason is not None:
                message += f'. It is being used by {self._lockReason}'
            raise AssertionError(message)
        elif self._modLock:
            self._modLock = None
        self._config.updateConfig(config)

    # importDeviceConfig
    # exportNetwork - again seems like a utility method
    # saveNetwork - idea is to save this network configuration to the UserAccount
