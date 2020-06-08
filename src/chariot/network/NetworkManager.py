from typing import Dict
from chariot.network import Network
from chariot.utility import Manager


class _NetworkManager(Manager):

    def __init__(self):
        self.collection: Dict[str, Network] = {}

    def addNetwork(self, network: Network) -> None:
        self._addToCollection(network)

    def deleteNetwork(self, networkName: str) -> None:
        self._deleteFromCollection(networkName)

    def getNetwork(self, networkName: str) -> Network:
        return self._retrieveFromCollection(networkName)

    # This method gives a new network name to an already defined network and updates the collection
    def replaceNetwork(self, toFind: str, newName: str):
        self._modifyNameInCollection(toFind, newName)

    # Returns a list of networks names found in the userNetworks
    def getAllNetworks(self) -> Dict[str, str]:
        allNetworks: Dict[str, str] = {}
        for key in self.collection:
            allNetworks[key] = self._retrieveFromCollection(key).getDescription()

        return allNetworks

    def getNetworksAndDevices(self):
        allNetworks = []

        for key in self.collection:
            description: str = ""
            try:
                description = self._retrieveFromCollection(key).getDescription()
            except:
                pass

            networkSpecifics: Dict[str, str] = \
                {'NetworkName': key,
                 'Description': description,
                 'Devices': self._retrieveFromCollection(key).getDeviceNames()
                 }
            allNetworks.append(networkSpecifics)

        return allNetworks

    def clearCollection(self):
        self._clearCollection()


# return a singleton instance
NetworkManager = _NetworkManager()

__all__ = ['NetworkManager']
