from typing import Dict, List
from flask import Flask, request, app, jsonify, request
from chariot.utility.exceptions.NoIdentifierError import NoIdentifierError
from chariot.utility.exceptions.DuplicateNameError import DuplicateNameError
from chariot.utility.exceptions.ErrorStrings import ErrorStrings
from chariot.utility.exceptions.NameNotFoundError import NameNotFoundError
from chariot.network.Network import Network


class _NetworkManager:

    def __init__(self):
        # TODO: load all networks for a user upon instantiation
        self.userNetworks: Dict[str, Network] = {}

    # This method gives a new network name to an already defined network. Find the network by name
    def modifyNetworkNameByName(self, newName: str, toFind: str):
        # check that newName is unique to avoid data overwrites
        if not self.isNetworkNameUnique(newName):
            raise DuplicateNameError(
                ErrorStrings.ERR_Not_Unique_Network_Name.value.format(newName)
            )

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
            raise NoIdentifierError(ErrorStrings.ERR_Specify_Network_Identifier)

        # When adding a key, if the same key is in the dict, the values are overriden. Avoid this.
        if self.isNetworkNameUnique(networkName):
            network = Network(networkName, networkDesc)
            self.userNetworks[networkName] = network
        else:
            raise DuplicateNameError(ErrorStrings.ERR_Not_Unique_Network_Name.value.format(networkName))

    # This method deletes a Network object via name from the nested dictionary of Networks that this class manages
    def deleteNetworkByName(self, netName: str):
        networkToDel: Network = self.findNetworkByNetworkName(netName)
        if networkToDel is not None:
            del self.userNetworks[networkToDel.getNetworkName()]

    # Convenience method used to return a Network object via a given network name
    def findNetworkByNetworkName(self, netNameToFind: str) -> Network:
        # since the collection is nested dictionaries, find the name with .get()
        try:
            network: Network = self.userNetworks[netNameToFind]
        except KeyError:
            raise NameNotFoundError(ErrorStrings.ERR_Network_Not_Found_In_Collection.value.format(netNameToFind))
        return network

    # Convenience method that checks whether a network by the same name exists in the collection
    def isNetworkNameUnique(self, uniqueName: str) -> bool:
        unique: bool
        if uniqueName not in self.userNetworks:
            unique = True
        else:
            unique = False
        return unique

    # Returns a list of networks names found in the userNetworks
    def getAllNetworkNamesAndDesc(self) -> Dict[str, str]:
        allNetworks: Dict[str, str] = {}
        for key in self.userNetworks:
            allNetworks[key] = self.findNetworkByNetworkName(key).getNetworkDesc()

        return allNetworks

    def getAllNetworkNamesAndDevices(self):
        allNetworks = []

        for key in self.userNetworks:
            networkSpecifics: Dict[str, str] = \
                {'NetworkName': key,
                 'Description': self.findNetworkByNetworkName(key).getNetworkDesc(),
                 'Devices': self.findNetworkByNetworkName(key).getAllDeviceNamesOnNetwork()
                 }
            allNetworks.append(networkSpecifics)

        return allNetworks
    # def importNetworkConfiguration
    # def exportNetworkConfiguration
    # https://blog.miguelgrinberg.com/index/page/3


# return a singleton instance
NetworkManager = _NetworkManager()

__all__ = ['NetworkManager']
