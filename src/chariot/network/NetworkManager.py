from typing import Dict, List
from flask import Flask, request, app, jsonify, request

from chariot.network.Network import Network


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
            # throw error saying that name is not unique
            pass

        network: Network = self.findNetworkByNetworkName(toFind)

        if network is not None:
            # update network instance
            network.modifyNetworkName(newName)
            # update collection, make new key and delete the old one
            self.userNetworks[network.getNetworkName()] = self.userNetworks[toFind]
            del self.userNetworks[toFind]
        else:
            # throw exception that network name is not found in collection
            pass

    # This method modifies a network's description.
    def modifyNetworkDescriptionByName(self, newDesc: str, networkName: str):
        network: Network = self.findNetworkByNetworkName(networkName)
        if network is not None:
            network.modifyNetworkDesc(newDesc)
        else:
            # throw exception that network name is not found in collection
            pass

    # This method adds a Network object to the dictionary of Networks that this class manages
    def addNetwork(self, networkName: str, networkDesc: str):
        if networkName is None:
            # raise expection here
            pass

        # When adding a key, if the same key is in the dict, the values are overriden. Avoid this.
        if self.isNetworkNameUnique(networkName):
            network = Network(networkName, networkDesc)
            self.userNetworks[networkName] = network
        else:
            # network name is not unique, throw correct exception
            pass

    # This method deletes a Network object via name from the nested dictionary of Networks that this class manages
    def deleteNetworkByName(self, netName: int):
        networkToDel: Network = self.findNetworkByNetworkName(netName)
        if networkToDel is not None:
            del self.userNetworks[networkToDel.getNetworkName()]

    # Convenience method used to return a Network object via a given network name
    def findNetworkByNetworkName(self, netNameToFind: str) -> Network:
        # since the collection is nested dictionaries, find the name with .get()
        try:
            network: Network = self.userNetworks.get(netNameToFind)
        except KeyError:
            # figure out best way to handle
            pass
        return network

    # Convenience method that checks whether a network by the same name exists in the collection
    def isNetworkNameUnique(self, uniqueName: str) -> bool:
        found: bool = False
        if self.findNetworkByNetworkName(uniqueName) is not None:
            found = True
        return found

    # Returns a list of networks names found in the userNetworks
    def getAllNetworkNames(self) -> List[str]:
        allNames: List[str] = []
        for key in self.userNetworks:
            allNames.append(key)

        return allNames

    # def importNetworkConfiguration
    # def exportNetworkConfiguration
    # https://blog.miguelgrinberg.com/index/page/3
