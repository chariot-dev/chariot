import signal

from chariot.network import NetworkManager, Network


class DataCollectionManager:
    # This class is intended to work with an instance of NetworkManager. The NetworkManager
    # is responsible for housing multiple user-defined networks. Once a network has been selected
    # for data collection, this class interacts with the NetworkManager to start and stop data collection
    # of all devices from the selected network

    def __init__(self, networkManager: NetworkManager):
        self.networkManager = networkManager
        self.activeNetwork: Network = self.networkManager.getNetworkByIndex(0)  # default network to use

    def setActiveNetwork(self, networkToUse: str):
        self.activeNetwork = self.networkManager.findNetworkByNetworkName(networkToUse)

    def getActiveNetwork(self) -> Network:
        return self.activeNetwork

    # This method starts the data collection process for all devices on the selected network.
    # Simply iterate through the Network to get to the device and sends a start signal
    def collectData(self, networkToUse: str):
        # find the Network by unique network name
        chosenNetwork: Network = self.networkManager.findNetworkByNetworkName(networkToUse)

        if chosenNetwork is not None:
            self.activeNetwork = chosenNetwork  # update active network
            # iterate the network collection and start device interaction
            for device in chosenNetwork.getAllDevices():
                device.startDataCollection()

    # This method stops the data collection process for all devices on the selected network.
    # Simply iterate through the Network to get to the device and sends a stop signal
    def terminateDataCollection(self):
        for device in self.activeNetwork.getAllDevices():
            device.stopDataCollection()

    # This method is to handle ctrl-c in a graceful manner.
    # NOTE: Python signal handlers are always executed in the main Python thread
    #def handler(signum, frame):
        # Handle cleanup which is gracefully terminating data collection
        #print("SIGINT detected. Closing application.")
        #self.terminateDataCollection()


# Set the signal handler
#signal.signal(signal.CTRL_C_EVENT, handler)

