from threading import Thread
# unused right now, but will be useful for scaling past a couple of devices
from multiprocessing.queues import Queue as ProcessQueue
from typing import Dict
from sys import exc_info
from time import time
from queue import Empty as QueueEmptyException, Queue as ThreadQueue
from chariot.collection import DataCollector
from chariot.device.adapter import DeviceAdapter
from chariot.utility import Manager
from chariot.utility.JSONTypes import JSONObject
from chariot.network import Network
from chariot.database.writer import DatabaseWriter
from chariot.utility.exceptions.ChariotExceptions import *


class DataCollectionManager(Manager):
    # This class is intended to work with an instance of NetworkManager. The NetworkManager
    # is responsible for housing multiple user-defined networks. Once a network has been selected
    # for data collection, this class interacts with the NetworkManager to start and stop data collection
    # of all devices from the selected network
    
    def __init__(self):
        self.collection = Dict[str, DataCollector] = {}

    def addCollector(self, collector: DataCollector) -> None:
        self._addToCollection(collector)

    def deleteCollector(self, collectorName: str) -> None:
        self._deleteFromCollection(collectorName)
    
    def getCollector(self, collectorName: str) -> DataCollector:
        return self._retrieveFromCollection(collectorName)
    
    def getCollectors(self) -> Dict[str, str]:
        collectors: Dict[str, str] = { name: item.getDescription() for name, item in self.collection.items() }
        return collectors
    
    def replaceCollector(self, newName: str, collectorName: str) -> None:
        self._modifyNameInCollection(newName, collectorName)
