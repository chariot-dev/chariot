from typing import Dict, List
from flask import Flask, request, app, jsonify, request
from src.chariot.utility.exceptions import DuplicateNameError, NameNotFoundError, NoIdentifierError
from src.chariot.network.Network import Network


class NetworkManager:
    __instance = None

    @staticmethod
    def getInstance(cls):
        if NetworkManager.__instance is None:
            NetworkManager()
        return NetworkManager.__instance

    def __init__(self):
        # TODO: load all networks for a user upon instantiation
        if NetworkManager.__instance is None:
            # hold all user defined networks. This will be a dictionary in which
            # each key is the name of the network (Network names are unique).
            self.userNetworks: Dict[str, Network] = {}
            NetworkManager.__instance = self

    # This method gives a new network name to an already defined network. Find the network by name
    def modifyNetworkNameByName(self, newName: str, toFind: str):
        # check that newName is unique to avoid data overwrites
        if self.isNetworkNameUnique(newName) is False:
            raise DuplicateNameError(newName, 'Network')

        network: Network = self.findNetworkByNetworkName(toFind)

        # update network instance
        network.modifyNetworkName(newName)
        # update collection, make new key and delete the old one
        self.userNetworks[network.getNetworkName()] = self.userNetworks[toFind]
        del self.userNetworks[toFind]

    # This method modifies a network's description.
    def modifyNetworkDescriptionByName(self, newDesc: str, networkName: str):
        network: Network = self.findNetworkByNetworkName(networkName)
        network.modifyNetworkDesc(newDesc)

    # This method adds a Network object to the dictionary of Networks that this class manages
    def addNetwork(self, networkName: str, networkDesc: str):
        if networkName is None:
            raise NoIdentifierError('Network')

        # When adding a key, if the same key is in the dict, the values are overriden. Avoid this.
        if self.isNetworkNameUnique(networkName):
            network = Network(networkName, networkDesc)
            self.userNetworks[networkName] = network
        else:
            raise DuplicateNameError(networkName, 'Network')

    # This method deletes a Network object via name from the nested dictionary of Networks that this class manages
    def deleteNetworkByName(self, netName: int):
        networkToDel: Network = self.findNetworkByNetworkName(netName)
        if networkToDel is not None:
            del self.userNetworks[networkToDel.getNetworkName()]
        else:
            raise NameNotFoundError('Network', netName, 'known networks')

    # Convenience method used to return a Network object via a given network name
    def findNetworkByNetworkName(self, netNameToFind: str) -> Network:
        try:
            network: Network = self.userNetworks[netNameToFind]
        except KeyError:
            raise NameNotFoundError('Network', netNameToFind, 'known networks')
        return network

    # Convenience method that checks whether a network by the same name exists in the collection
    def isNetworkNameUnique(self, uniqueName: str) -> bool:
        found: bool = False
        if self.findNetworkByNetworkName(uniqueName) is not None:
            found = True
        return found

    # Returns a list of networks names found in the userNetworks
    def getAllNetworkNamesAndDesc(self) -> Dict[str, str]:
        allNetworks: Dict[str, str] = {}
        for key in self.userNetworks:
            allNetworks[key] = self.findNetworkByNetworkName(key).getNetworkDesc()

        return allNetworks

    # def importNetworkConfiguration
    # def exportNetworkConfiguration
    # https://blog.miguelgrinberg.com/index/page/3
