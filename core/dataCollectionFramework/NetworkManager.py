from typing import List

from core.dataCollectionFramework import Network


class NetworkManager:
    # userNetworks: List[Network] = [] #hold all user defined networks

    def __init__(self):
        self.userNetworks: List[Network] = []  # hold all user defined networks

    # This method gives a new network name to an already defined network. Find the network by name
    def modifyNetworkNameByName(self, newName: str, toFind: str):
        network: Network = self.findNetworkByNetworkName(toFind)
        if network:
            network.modifyNetworkName(newName)

    # This method gives a new network name to an already defined network. Find the network by name
    def modifyNetworkNameByIndex(self, newName: str, index: int):
        self.userNetworks[index].modifyNetworkName(newName)

    def modifyNetworkDescriptionByName(self, newDesc: str, networkName: str):
        network: Network = self.findNetworkByNetworkName(networkName)
        if network:
            network.modifyNetworkDesc(newDesc)

    def modifyNetworkDescriptionByIndex(self, newDesc: str, index: int, ):
        if index - 1 > len(self.userNetworks) or index < 0:
            print("Invalid index given for deletion of network.")
        else:
            self.userNetworks[index].modifyNetworkDesc(newDesc)

    # This method adds a Network object to the list of Networks that this class manages
    #   this version of adding a Network just appends to the end
    def addNetwork(self, network: Network):
        self.userNetworks.append(network)

    # This method deletes a Network object via index from list of Networks that this class manages
    def deleteNetworkByIndex(self, index: int):
        if index - 1 > len(self.userNetworks) or index < 0:
            print("Invalid index given for deletion of network.")
        else:
            del self.userNetworks[index - 1]

    # This method deletes a Network object via name from list of Networks that this class manages
    def deleteNetworkByName(self, netName: int):
        # iterate through list and find the network name to delete
        startingLength: int = len(self.userNetworks)
        i: int = 0
        while i < len(self.userNetworks):
            if self.userNetworks[i].getNetworkName() == netName:
                del self.userNetworks[i]
        if startingLength == len(self.userNetworks):
            print('{} not found in collection. Deletion unsuccessful!', netName)

    # Convenience method used to return a Network object via a given network name
    # TODO: figure out best way to return if Network is not found
    def findNetworkByNetworkName(self, netName: str) -> Network:
        i: int = 0
        while i < len(self.userNetworks):
            if self.userNetworks[i].getNetworkName() == netName:
                return self.userNetworks[i]

    def getNetworkByIndex(self, index: int) -> Network:
        if index - 1 > len(self.userNetworks) or index < 0:
            print("Invalid index given for deletion of network.")
        else:
            return self.userNetworks[index]

    #def importNetworkConfiguration
    #def exportNetworkConfiguration