import pytest
from typing import List, Optional
from chariot.collection import DataCollectionManager, DataCollector
from chariot.collection.configuration import DataCollectionConfiguration
from chariot.database.configuration import DatabaseConfiguration
from chariot.network import Network
from chariot.network.configuration import NetworkConfiguration
from chariot.utility.exceptions import DuplicateNameError, NameNotFoundError
from chariot.utility.JSONTypes import JSONObject
from test.testutils import TestDatabaseWriter


class DataCollectionManagerTest:
    instance: Optional[DataCollectionManager] = None
    collector: Optional[DataCollector] = None

    def setup_method(self):
        self.instance = DataCollectionManager()
        self.collector = self.makeCollector('Test Collector 1')

    def makeCollector(self, collectorName: str) -> DataCollector:
        networkConfigJson: JSONObject = {
            'networkName': 'Network 1',
            'description': 'Sample network'
        }
        networkConfig: NetworkConfiguration = NetworkConfiguration(networkConfigJson)
        network: Network = Network(networkConfig)

        dbConfigJson: JSONObject = {
            'dbId': 'Test Database',
            'databaseName': 'TestData',
            'type': 'TestDB',
            'host': '127.0.0.1',
        }
        dbConfig: DatabaseConfiguration = DatabaseConfiguration(dbConfigJson)
        dbWriter: TestDatabaseWriter = TestDatabaseWriter(dbConfig)

        collectorConfigJson: JSONObject = {
            'configId': collectorName,
            'network': network,
            'database': dbWriter,
            'runTime': 10000,
        }
        collectorConfig: DataCollectionConfiguration = DataCollectionConfiguration(collectorConfigJson)
        collector: DataCollector = DataCollector(collectorConfig)
        return collector

    def addCollectorTest(self):
        self.instance.addCollector(self.collector)
        collectors: List[DataCollector] = self.instance.getCollectors()
        assert len(collectors) == 1
        assert collectors[0] == self.collector

    def deleteCollectorTest(self):
        self.instance.addCollector(self.collector)
        collectors: List[DataCollector] = self.instance.getCollectors()
        assert len(collectors) == 1
        self.instance.deleteCollector('Test Collector 1')
        collectors = self.instance.getCollectors()
        assert len(collectors) == 0

    def getCollectorTest(self):
        self.instance.addCollector(self.collector)
        assert self.instance.getCollector('Test Collector 1') == self.collector

    def getCollectorsTest(self):
        self.instance.addCollector(self.collector)
        collector2: DataCollector = self.makeCollector('Test Collector 2')
        self.instance.addCollector(collector2)
        collectors: List[DataCollector] = self.instance.getCollectors()
        assert len(collectors) == 2
        assert collectors[0] == self.collector
        assert collectors[1] == collector2

    def replaceCollectorTest(self):
        collector2: DataCollector = self.makeCollector('Test Collector 2')
        self.instance.addCollector(self.collector)
        self.instance.addCollector(collector2)
        with pytest.raises(DuplicateNameError):
            self.instance.replaceCollector('Test Collector 1', 'Test Collector 2')
        self.instance.replaceCollector('Test Collector 1', 'Test Collector A')
        with pytest.raises(NameNotFoundError):
            self.instance.getCollector('Test Collector 1')
        collector: DataCollector = self.instance.getCollector('Test Collector A')
        assert collector.getConfiguration().configId == 'Test Collector A'
