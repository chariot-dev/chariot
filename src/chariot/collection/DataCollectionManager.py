from typing import Dict, List, Union
from chariot.collection import DataCollector
from chariot.utility import Manager
from chariot.utility.JSONTypes import JSONObject


class _DataCollectionManager(Manager):
    # This class is intended to work with an instance of NetworkManager. The NetworkManager
    # is responsible for housing multiple user-defined networks. Once a network has been selected
    # for data collection, this class interacts with the NetworkManager to start and stop data collection
    # of all devices from the selected network

    def __init__(self):
        self.collection: Dict[str, DataCollector] = {}

    def addCollector(self, collector: DataCollector) -> None:
        self._addToCollection(collector)

    def deleteCollector(self, collectorName: str) -> None:
        self._deleteFromCollection(collectorName)

    def getCollector(self, collectorName: str) -> DataCollector:
        return self._retrieveFromCollection(collectorName)

    def _getCollectorsJson(self) -> Dict[str, JSONObject]:
        # will implement when Network and DatabaseWriter issue is resolved
        return {}

    def getCollectors(self, json=False) -> [Union[List[DataCollector], Dict[str, JSONObject]]]:
        if json:
            return self._getCollectorsJson()
        return [collector for collector in self.collection.values()]

    def replaceCollector(self, collectorName: str, newName: str) -> None:
        self._modifyNameInCollection(collectorName, newName)


# return a singleton instance
DataCollectionManager = _DataCollectionManager()

__all__ = ['DataCollectionManager']
